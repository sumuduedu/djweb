# apps/enrollment/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from apps.courses.models import Course
from apps.batch.models import Batch
from apps.accounts.models import Student, Parent
from .models import EnrollmentInquiry, Enrollment


# ================================
# 🔐 ADMIN CHECK
# ================================
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return hasattr(user, 'profile') and user.profile.role in ['ADMIN', 'STAFF']


# ================================
# 📋 APPLICATION LIST (ADMIN)
# ================================
class ApplicationListView(AdminRequiredMixin, ListView):
    model = EnrollmentInquiry
    template_name = "enrollment/application_list.html"
    context_object_name = "applications"
    ordering = ['-created_at']

    def get_queryset(self):
        return EnrollmentInquiry.objects.select_related('user', 'course')


# ================================
# 📝 APPLY (UNIFIED)
# ================================
class ApplyView(LoginRequiredMixin, View):

    template_name = "enrollment/apply.html"

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        application = EnrollmentInquiry.objects.filter(
            user=request.user,
            course=course
        ).first()

        return render(request, self.template_name, {
            "course": course,
            "application": application,
        })

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        role_type = request.POST.get("role_type")

        application = EnrollmentInquiry.objects.filter(
            user=user,
            course=course
        ).first()

        # 🚫 BLOCK if active
        if application and application.status in ['PENDING', 'APPROVED']:
            messages.warning(request, "You already have an active application.")
            return redirect('core:dashboard')

        data = {
            "phone": request.POST.get("phone"),
            "home_phone": request.POST.get("home_phone"),
            "current_address": request.POST.get("current_address"),
            "permanent_address": request.POST.get("permanent_address"),
            "qualification": request.POST.get("qualification"),
            "nic_number": request.POST.get("nic_number"),
            "nic_copy": request.FILES.get("nic_copy"),
            "notes": request.POST.get("notes"),
        }

        if role_type == "PARENT":
            data.update({
                "parent_name": request.POST.get("parent_name"),
                "parent_email": request.POST.get("parent_email"),
                "student_name": request.POST.get("student_name"),
                "student_age": request.POST.get("student_age") or None,
                "relationship": request.POST.get("relationship"),
            })

        # 🔁 REAPPLY
        if application and application.status == 'REJECTED':
            for k, v in data.items():
                if v:
                    setattr(application, k, v)

            application.role_type = role_type
            application.status = 'PENDING'
            application.current_stage = 'SUBMITTED'
            application.rejection_reason = None
            application.is_nic_verified = False

            application.save()

            messages.success(request, "Application resubmitted.")
            return redirect('core:dashboard')

        # 🆕 CREATE
        EnrollmentInquiry.objects.create(
            user=user,
            course=course,
            role_type=role_type,
            full_name=user.get_full_name(),
            email=user.email,
            current_stage='SUBMITTED',
            **data
        )

        messages.success(request, "Application submitted successfully.")
        return redirect('core:dashboard')


# ================================
# ✅ APPROVE APPLICATION
# ================================
class ApproveApplicationView(AdminRequiredMixin, View):

    def post(self, request, pk):
        app = get_object_or_404(EnrollmentInquiry, id=pk)

        if app.status != 'PENDING':
            messages.warning(request, "Already processed.")
            return redirect('enrollment:application_list')

        user = app.user
        profile = user.profile

        # 📊 Move stage
        app.current_stage = 'FINAL'

        # 🎓 assign role
        profile.role = app.role_type
        profile.save()

        student = None

        # ====================
        # STUDENT FLOW
        # ====================
        if app.role_type == 'STUDENT':
            student = user.student

        # ====================
        # PARENT FLOW
        # ====================
        elif app.role_type == 'PARENT':

            username = app.student_name.lower().replace(" ", "")
            while User.objects.filter(username=username).exists():
                username += "1"

            password = User.objects.make_random_password()

            student_user = User.objects.create(username=username)
            student_user.set_password(password)
            student_user.save()

            student = Student.objects.create(
                user=student_user,
                full_name=app.student_name
            )

            parent, _ = Parent.objects.get_or_create(user=user)
            student.parents.add(parent)

            app.parent_user = user

            # 📧 send credentials
            send_mail(
                "Student Account Created",
                f"Username: {username}\nPassword: {password}",
                settings.DEFAULT_FROM_EMAIL,
                [app.parent_email or app.email],
                fail_silently=True,
            )

        # ====================
        # ENROLL TO BATCH
        # ====================
        batch_id = request.POST.get('batch_id')
        if batch_id:
            batch = get_object_or_404(Batch, id=batch_id)

            if batch.course != app.course:
                messages.error(request, "Invalid batch.")
                return redirect('enrollment:application_list')

            try:
                Enrollment.objects.create(student=student, batch=batch)
            except IntegrityError:
                messages.warning(request, "Already enrolled.")

        # ====================
        # FINALIZE
        # ====================
        app.status = 'APPROVED'
        app.save()

        # 📧 notify
        send_mail(
            "Application Approved",
            f"Dear {app.full_name}, your application is approved.",
            settings.DEFAULT_FROM_EMAIL,
            [app.email],
            fail_silently=True,
        )

        messages.success(request, "Application approved.")
        return redirect('enrollment:application_list')


# ================================
# ❌ REJECT APPLICATION
# ================================
class RejectApplicationView(AdminRequiredMixin, View):

    def post(self, request, pk):
        app = get_object_or_404(EnrollmentInquiry, id=pk)

        reason = request.POST.get("reason")

        if not reason:
            messages.error(request, "Reason required.")
            return redirect('enrollment:application_list')

        app.status = 'REJECTED'
        app.current_stage = 'FINAL'
        app.rejection_reason = reason
        app.save()

        send_mail(
            "Application Rejected",
            f"Dear {app.full_name},\n\nReason:\n{reason}",
            settings.DEFAULT_FROM_EMAIL,
            [app.email],
            fail_silently=True,
        )

        messages.error(request, "Application rejected.")
        return redirect('enrollment:application_list')


# ================================
# 🔐 CHANGE STUDENT PASSWORD
# ================================
class ChangeStudentPasswordView(LoginRequiredMixin, View):

    def post(self, request):
        parent = request.user.parent
        student_user = parent.student.user

        new_password = request.POST.get("password")

        student_user.password = make_password(new_password)
        student_user.save()

        messages.success(request, "Student password updated.")
        return redirect('core:parent_dashboard')


# ================================
# 🔔 LIVE NOTIFICATIONS API
# ================================
@login_required
def notification_api(request):
    apps = EnrollmentInquiry.objects.filter(user=request.user)

    data = [
        {
            "course": a.course.title,
            "status": a.status,
            "stage": a.current_stage,
            "date": a.created_at.strftime("%Y-%m-%d"),
        }
        for a in apps
    ]

    return JsonResponse({"notifications": data})
