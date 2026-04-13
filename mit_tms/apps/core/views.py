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

from apps.accounts.models import Profile
from apps.website.models import Enrollment, ContactMessage
from .forms import CustomSignupForm

from django.contrib.auth import login

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

        # 🎯 Template helpers
        context["is_admin"] = self.profile.role == "ADMIN"
        context["is_teacher"] = self.profile.role == "TEACHER"
        context["is_student"] = self.profile.role == "STUDENT"

        # Optional related objects
        context["student"] = getattr(self.request.user, "student", None)
        context["teacher"] = getattr(self.request.user, "teacher", None)

        return context

class HomeView(TemplateView):
    template_name = "website/home.html"


class AdminDashboardView(BaseView):
    allowed_roles = ['ADMIN']
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        context['messages'] = ContactMessage.objects.order_by('-created_at')[:5]
        context['new_messages'] = ContactMessage.objects.filter(is_read=False).count()
        context['enrollments'] = Enrollment.objects.order_by('-created_at')[:5]

        return context

class StudentDashboardView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/student.html"

class TeacherDashboardView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teacher.html"
@login_required
def dashboard_redirect(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif profile.role == 'TEACHER':
        return redirect('teacher_dashboard')
    elif profile.role == 'STUDENT':
        return redirect('student_dashboard')

    return redirect('student_dashboard')   # 🔥 fallback

class SignupView(View):

    def get(self, request):
        return render(request, 'auth/signup.html', {
            'form': CustomSignupForm()
        })

    def post(self, request):
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # 🔐 Token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            domain = get_current_site(request).domain
            activation_link = f"http://{domain}/activate/{uid}/{token}/"

            # 📧 Email
            send_mail(
                subject="Activate Your Account",
                message=(
                    f"Hi {user.username},\n\n"
                    f"Click below to activate your account:\n\n"
                    f"{activation_link}\n\n"
                    f"If you didn't register, ignore this."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return render(request, 'auth/signup_success.html', {
                'email': user.email
            })

        return render(request, 'auth/signup.html', {'form': form})
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

            login(request, user)   # 🔥 AUTO LOGIN

            return redirect('dashboard')   # 🔥 go to dashboard

        return render(request, 'auth/activation_failed.html')

class StudentCoursesView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "student/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = self.request.user.student

        context['enrollments'] = Enrollment.objects.filter(student=student)

        return context


class StudentAttendanceView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "student/attendance.html"
