from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages

from apps.accounts.models import Profile


# ================================
# 👤 PROFILE VIEW
# ================================
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


# ================================
# ⚙️ ACCOUNT SETTINGS
# ================================
class AccountSettingsView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "accounts/settings.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)

        # 🔷 Update password
        password = self.request.POST.get("password")
        if password:
            user.set_password(password)

        user.save()

        # 🔥 SAFE PROFILE HANDLING (FIX)
        profile, created = Profile.objects.get_or_create(user=user)

        # 🔷 Handle image upload
        image = self.request.FILES.get("image")
        if image:
            profile.image = image
            profile.save()

        # 🔷 Success message
        messages.success(self.request, "Profile updated successfully")

        return super().form_valid(form)
