from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from .forms import CustomSignupForm, CustomLoginForm
from .models import Profile


# ================================
# 🔐 LOGIN VIEW
# ================================
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        return '/app/dashboard/'


# ================================
# 🔓 LOGOUT VIEW
# ================================
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# ================================
# 📝 SIGNUP VIEW
# ================================
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

            # create profile
            Profile.objects.get_or_create(user=user)

            # activation email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            domain = get_current_site(request).domain
            link = f"http://{domain}/accounts/activate/{uid}/{token}/"

            send_mail(
                subject="Activate your account",
                message=f"Click to activate:\n{link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return render(request, 'auth/signup_success.html', {
                'email': user.email
            })

        return render(request, 'auth/signup.html', {'form': form})


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
            return redirect('core:dashboard')

        return render(request, 'auth/activation_failed.html')


# ================================
# 🔐 ADMIN CHECK MIXIN
# ================================
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'ADMIN'


# ================================
# 👤 PROFILE VIEW
# ================================
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        profile = getattr(user, 'profile', None)

        context['profile'] = profile

        context['student'] = getattr(user, 'student', None)
        context['teacher'] = getattr(user, 'teacher', None)
        context['staff'] = getattr(user, 'staff', None)
        context['parent'] = getattr(user, 'parent', None)
        context['alumni'] = getattr(user, 'alumni', None)

        return context


# ================================
# ⚙️ ACCOUNT SETTINGS
# ================================
class AccountSettingsView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['role', 'image']
    template_name = "accounts/settings.html"
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():
            profile = form.save(commit=False)

            # 🔥 IMPORTANT: save uploaded file
            if request.FILES.get('image'):
                profile.image = request.FILES.get('image')

            profile.save()

            messages.success(request, "Settings updated successfully")
            return redirect(self.success_url)

        return self.form_invalid(form)


# ================================
# 👥 USER LIST
# ================================
class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        return User.objects.select_related('profile').order_by('-date_joined')


# ================================
# 👤 USER DETAIL
# ================================
class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    context_object_name = "user_obj"


# ================================
# ➕ USER CREATE
# ================================
from django import forms

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        Profile.objects.get_or_create(user=user)

        messages.success(self.request, "User created successfully")
        return super().form_valid(form)


# ================================
# ✏️ USER UPDATE
# ================================
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        user = form.save()

        profile = user.profile

        # 🔥 Handle image
        if self.request.FILES.get('image'):
            profile.image = self.request.FILES.get('image')

        # 🔥 Handle role
        role = self.request.POST.get('role')
        if role:
            profile.role = role

        profile.save()

        # 🔥 Handle password
        password = self.request.POST.get('password')
        if password:
            user.set_password(password)
            user.save()

        messages.success(self.request, "User updated successfully")
        return super().form_valid(form)


# ================================
# 🗑️ USER DELETE
# ================================
class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/user_confirm_delete.html"
    success_url = reverse_lazy('accounts:user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "User deleted successfully")
        return super().delete(request, *args, **kwargs)
