from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from apps.accounts.models import Profile
from apps.website.models import  ContactMessage
from apps.enrollment.models import EnrollmentInquiry

# ================================
# 🔁 DASHBOARD REDIRECT
# ================================
@login_required
def dashboard_redirect(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.role == 'ADMIN':
        return redirect('core:admin_dashboard')
    elif profile.role == 'STAFF':
        return redirect('core:staff_dashboard')
    elif profile.role == 'TEACHER':
        return redirect('core:teacher_dashboard')
    elif profile.role == 'STUDENT':
        return redirect('core:student_dashboard')
    elif profile.role == 'PARENT':
        return redirect('core:parent_dashboard')
    elif profile.role == 'ALUMNI':
        return redirect('core:alumni_dashboard')

    return redirect('core:guest_dashboard')

# ================================
# 🔷 BASE VIEW (ROLE CONTROL)
# ================================
class BaseView(LoginRequiredMixin, TemplateView):
    allowed_roles = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, _ = Profile.objects.get_or_create(user=request.user)

        # 🔐 Role restriction
        if self.allowed_roles and self.profile.role not in self.allowed_roles:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = self.profile
        context["role"] = self.profile.role

        # 🔥 Role flags (important for sidebar)
        context["is_admin"] = self.profile.role == "ADMIN"
        context["is_staff"] = self.profile.role == "STAFF"
        context["is_teacher"] = self.profile.role == "TEACHER"
        context["is_student"] = self.profile.role == "STUDENT"
        context["is_parent"] = self.profile.role == "PARENT"
        context["is_guest"] = self.profile.role == "GUEST"

        # Safe access
        context["student"] = getattr(self.request.user, "student", None)
        context["teacher"] = getattr(self.request.user, "teacher", None)

        return context


# ================================
# 🌐 HOME
# ================================
class HomeView(TemplateView):
    template_name = "website/home.html"


# ================================
# 👑 ADMIN DASHBOARD
# ================================
class AdminDashboardView(BaseView):
    allowed_roles = ['ADMIN']
    template_name = "dashboard/admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔹 Imports (kept inside as you prefer)
        from django.contrib.auth.models import User
        from apps.accounts.models import Student, Teacher
        from apps.enrollment.models import EnrollmentInquiry, Enrollment
        from apps.website.models import ContactMessage
        from apps.batch.models import Batch

        # ================================
        # 📊 SYSTEM STATS
        # ================================
        context['total_users'] = User.objects.count()
        context['total_students'] = Student.objects.count()
        context['total_teachers'] = Teacher.objects.count()
        context['pending_applications'] = EnrollmentInquiry.objects.filter(status='PENDING').count()

        # 🔥 ADD THESE (IMPORTANT)
        context['total_batches'] = Batch.objects.count()
        context['total_enrollments'] = Enrollment.objects.count()

        # ================================
        # 📋 RECENT DATA
        # ================================
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]

        context['applications'] = EnrollmentInquiry.objects.select_related(
            'user', 'course'
        ).order_by('-created_at')[:5]

        context['messages'] = ContactMessage.objects.order_by('-created_at')[:5]

        # 🔥 FIXED ENROLLMENTS (IMPORTANT)
        context['enrollments'] = Enrollment.objects.select_related(
            'student',
            'batch__course'
        ).order_by('-enrolled_at')[:5]

        # ================================
        # 🔔 NOTIFICATIONS
        # ================================
        context['new_messages'] = ContactMessage.objects.filter(is_read=False).count()

        return context
# ================================
# 🧑‍💼 STAFF DASHBOARD
# ================================
class StaffDashboardView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.enrollment.models import EnrollmentInquiry

        context['pending'] = EnrollmentInquiry.objects.filter(status='PENDING').count()
        context['approved'] = EnrollmentInquiry.objects.filter(status='APPROVED').count()
        context['rejected'] = EnrollmentInquiry.objects.filter(status='REJECTED').count()

        context['applications'] = EnrollmentInquiry.objects.order_by('-created_at')[:5]

        return context

# ================================
# 👨‍🏫 TEACHER DASHBOARD
# ================================
class TeacherDashboardView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teacher.html"


# ================================
# 🎓 STUDENT DASHBOARD
# ================================
from apps.core.gateway import get_student_enrollments


class StudentDashboardView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/student.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['enrollments'] = get_student_enrollments(self.request.user)

        return context
# ================================
# 👨‍👩‍👧 PARENT DASHBOARD
# ================================
class ParentDashboardView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parent.html"


# ================================
# 👤 GUEST DASHBOARD
# ================================
from apps.courses.models import Course

from apps.enrollment.models import EnrollmentInquiry

class GuestDashboardView(BaseView):
    allowed_roles = ['GUEST']
    template_name = "dashboard/guest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        courses = Course.objects.all()

        # 🔥 get all applications for this user
        user_apps = EnrollmentInquiry.objects.filter(
            user=self.request.user
        ).select_related('course')

        # 🔥 map: course_id → application
        app_dict = {app.course_id: app for app in user_apps}

        context['courses'] = courses
        context['applications'] = app_dict   # ✅ IMPORTANT

        return context
# ================================
# 🎓 STUDENT COURSES
# ================================
class StudentCoursesView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "student/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = getattr(self.request.user, "student", None)

        if student:
            from apps.core.gateway import get_student_enrollments
            context['enrollments'] = get_student_enrollments(self.request.user)
        else:
            context['enrollments'] = []

        return context


# ================================
# 📅 STUDENT ATTENDANCE
# ================================
class StudentAttendanceView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "student/attendance.html"


# ================================
# 🔓 ACTIVATE ACCOUNT
# ================================
class ActivateAccountView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            login(request, user)

            return redirect('core:dashboard')   # 🔥 smart redirect

        return render(request, 'auth/activation_failed.html')


class AlumniDashboardView(BaseView):
    allowed_roles = ['ALUMNI']
    template_name = "dashboard/alumni.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = getattr(self.request.user, "student", None)

        if student:
            context['enrollments'] = get_student_enrollments(self.request.user)
        else:
            context['enrollments'] = []

        return context


from apps.enrollment.models import EnrollmentInquiry

class StudentDashboardView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/student.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # 🎓 batch enrollments
        context['enrollments'] = get_student_enrollments(user)

        # 📋 approved applications
        context['approved_apps'] = EnrollmentInquiry.objects.filter(
            user=user,
            status='APPROVED'
        )

        return context
