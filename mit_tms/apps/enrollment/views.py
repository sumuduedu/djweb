# apps/enrollment/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.courses.models import Course
from .models import EnrollmentInquiry
from .services import enroll_student
from apps.batch.models import Batch
from apps.enrollment.models import Enrollment
# ================================
# 🎓 ENROLL TO BATCH
# ================================
@login_required
def enroll_view(request, batch_id):
    enroll_student(request.user, batch_id)
    return redirect("core:dashboard")


# ================================
# 🔐 ADMIN CHECK
# ================================
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        return hasattr(user, 'profile') and user.profile.role in ['ADMIN', 'STAFF']


# ================================
# 📋 APPLICATION LIST
# ================================
class ApplicationListView(AdminRequiredMixin, ListView):
    model = EnrollmentInquiry
    template_name = "enrollment/application_list.html"
    context_object_name = "applications"
    ordering = ['-created_at']

    def get_queryset(self):
        return EnrollmentInquiry.objects.select_related('user', 'course')


# ================================
# ✅ APPROVE (POST)
# ================================
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

from apps.accounts.models import Student, Parent
from .models import EnrollmentInquiry
from django.db import IntegrityError

class ApproveApplicationView(AdminRequiredMixin, View):

    def post(self, request, pk):
        app = get_object_or_404(EnrollmentInquiry, id=pk)

        if app.status != 'PENDING':
            messages.warning(request, "This application has already been processed.")
            return redirect('enrollment:application_list')

        user = app.user
        profile = user.profile

        # 🔽 GET SELECTED BATCH
        batch_id = request.POST.get('batch_id')
        batch = None

        if batch_id:
            batch = get_object_or_404(Batch, id=batch_id)

            # 🔐 SECURITY CHECK
            if batch.course != app.course:
                messages.error(request, "Invalid batch selected.")
                return redirect('enrollment:application_list')

        # ============================
        # 🔥 UPDATE ROLE
        # ============================
        profile.role = app.role_type
        profile.save()

        student = None  # we’ll assign later

        # ============================
        # 🎓 STUDENT
        # ============================
        if app.role_type == 'STUDENT':
            student = user.student  # assuming OneToOne

        # ============================
        # 👨‍🏫 TEACHER
        # ============================
        elif app.role_type == 'TEACHER':
            pass  # handled elsewhere

        # ============================
        # 👨‍👩‍👧 PARENT → CREATE CHILD STUDENT
        # ============================
        elif app.role_type == 'PARENT':

            base_username = app.student_name.lower().replace(" ", "")
            username = base_username
            counter = 1

            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            student_user = User.objects.create(
                username=username,
                is_active=True
            )
            student_user.set_password("12345678")  # ⚠️ change later
            student_user.save()

            student = Student.objects.create(
                user=student_user,
                full_name=app.student_name
            )

            parent, _ = Parent.objects.get_or_create(user=user)
            student.parents.add(parent)

        # ============================
        # 🎯 CREATE ENROLLMENT (NEW)
        # ============================
        if student and batch:
            try:
                Enrollment.objects.create(
                    student=student,
                    batch=batch
                )
            except IntegrityError:
                messages.warning(request, "Student already enrolled in this batch.")

        # ============================
        # ✅ FINALIZE
        # ============================
        app.status = 'APPROVED'
        app.save()

        messages.success(request, "Application approved successfully.")
        return redirect('enrollment:application_list')

from django.contrib.auth.hashers import make_password

class ChangeStudentPasswordView(LoginRequiredMixin, View):

    def post(self, request):
        parent = request.user.parent
        student_user = parent.student.user

        new_password = request.POST.get("password")

        student_user.password = make_password(new_password)
        student_user.save()

        messages.success(request, "Student password updated")
        return redirect('core:parent_dashboard')

# ================================
# ❌ REJECT (POST)
# ================================
from django.core.mail import send_mail
from django.conf import settings

class RejectApplicationView(AdminRequiredMixin, View):

    def post(self, request, pk):
        app = get_object_or_404(EnrollmentInquiry, id=pk)

        if app.status != 'PENDING':
            messages.warning(request, "Already processed")
            return redirect('enrollment:application_list')

        reason = request.POST.get("reason")

        if not reason:
            messages.error(request, "Rejection reason is required.")
            return redirect('enrollment:application_list')

        # 🔴 Update status
        app.status = 'REJECTED'
        app.rejection_reason = reason
        app.save()

        # 📧 SEND EMAIL
        send_mail(
            subject="Application Rejected",
            message=f"""
Dear {app.full_name},

Your application for "{app.course.title}" has been rejected.

Reason:
{reason}

Please contact us for more information.

Thank you.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[app.email],
            fail_silently=True,
        )

        messages.error(request, "Application rejected and email sent.")
        return redirect('enrollment:application_list')
# ================================
# 🎓 APPLY STUDENT
# ================================
class ApplyStudentView(LoginRequiredMixin, View):

    template_name = "enrollment/apply_student.html"

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        application = EnrollmentInquiry.objects.filter(
            user=user,
            course=course
        ).order_by('-created_at').first()

        return render(request, self.template_name, {
            "course": course,
            "application": application
        })

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # 🚫 BLOCK ANY existing application (IMPORTANT CHANGE)
        if EnrollmentInquiry.objects.filter(user=user, course=course).exists():
            messages.warning(request, "You have already applied for this course.")
            return redirect('core:dashboard')

        # 🆕 New application only
        EnrollmentInquiry.objects.create(
            user=user,
            course=course,
            role_type='STUDENT',
            full_name=user.get_full_name(),
            email=user.email,
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            qualification=request.POST.get("qualification"),
        )

        messages.success(request, "Application submitted successfully!")
        return redirect('core:dashboard')


# ================================
# 👨‍👩‍👧 APPLY PARENT (placeholder)
# ================================
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from apps.courses.models import Course
from .models import EnrollmentInquiry


class ApplyParentView(LoginRequiredMixin, View):

    template_name = "enrollment/apply_parent.html"

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        application = EnrollmentInquiry.objects.filter(
            user=request.user,
            course=course
        ).order_by('-created_at').first()

        return render(request, self.template_name, {
            "course": course,
            "application": application
        })

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # 🚫 STRICT: block if already applied
        if EnrollmentInquiry.objects.filter(user=user, course=course).exists():
            messages.warning(request, "You have already applied for this course.")
            return redirect('core:dashboard')

        # 🆕 Create parent application
        EnrollmentInquiry.objects.create(
            user=user,
            course=course,
            role_type='PARENT',

            full_name=user.get_full_name(),
            email=user.email,

            phone=request.POST.get("phone"),
            address=request.POST.get("address"),

            # 👨‍👩‍👧 Parent-specific fields
            student_name=request.POST.get("student_name"),
            student_age=request.POST.get("student_age"),
            relationship=request.POST.get("relationship"),

            # optional
            notes=request.POST.get("notes"),
        )

        messages.success(request, "Parent application submitted successfully!")
        return redirect('core:dashboard')

