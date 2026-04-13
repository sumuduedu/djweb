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
from django.urls import reverse

from .forms import CustomSignupForm
from apps.website.models import Enrollment



# ===============================
# HOME PAGE
# ===============================
class HomeView(TemplateView):
    template_name = "website/home.html"


# ===============================
# DASHBOARD (LOGIN REQUIRED)
# ===============================
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.website.models import ContactMessage


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ✅ Recent Users
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]

        # ✅ Contact Messages (latest 5)
        context['messages'] = ContactMessage.objects.order_by('-created_at')[:5]

        # ✅ New Messages Count
        context['new_messages'] = ContactMessage.objects.filter(is_read=False).count()
        context['enrollments'] = Enrollment.objects.order_by('-created_at')[:5]

        return context

# ===============================
# SIGNUP VIEW (EMAIL ACTIVATION)
# ===============================
class SignupView(View):

    def get(self, request):
        form = CustomSignupForm()
        return render(request, 'auth/signup.html', {'form': form})

    def post(self, request):
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False   # 🔥 disable until email verified
            user.save()

            # 🔐 Generate token + UID
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # 🌐 Build activation URL
            domain = get_current_site(request).domain
            activation_link = f"http://{domain}/activate/{uid}/{token}/"

            # 📧 Send email
            send_mail(
                subject="Activate Your Account",
                message=f"Hi {user.username},\n\n"
                        f"Please click the link below to activate your account:\n\n"
                        f"{activation_link}\n\n"
                        f"If you did not register, please ignore this email.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return render(request, 'auth/signup_success.html', {
                'email': user.email
            })

        return render(request, 'auth/signup.html', {'form': form})


# ===============================
# ACTIVATE ACCOUNT VIEW
# ===============================
class ActivateAccountView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            return render(request, 'auth/activation_success.html')

        return render(request, 'auth/activation_failed.html')




