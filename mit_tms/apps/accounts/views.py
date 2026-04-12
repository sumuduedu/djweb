from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .models import Profile


# ================================
# 🔷 BASE VIEW
# ================================
class BaseView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile, _ = Profile.objects.get_or_create(user=self.request.user)

        context["profile"] = profile
        return context


# ================================
# 👤 PROFILE
# ================================
class ProfileView(BaseView):
    template_name = "accounts/profile.html"


# ================================
# ⚙️ SETTINGS
# ================================
class AccountSettingsView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "accounts/settings.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.object

        password = self.request.POST.get("password")
        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(self.request, user)

        profile, _ = Profile.objects.get_or_create(user=user)

        image = self.request.FILES.get("image")
        if image:
            profile.image = image
            profile.save()

        messages.success(self.request, "Profile updated successfully")

        return response

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from apps.accounts.models import Profile


# ================================
# 👤 USER LIST
# ================================
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView

class UserListView(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query)
            )

        return queryset


# ================================
# 👤 USER DETAIL
# ================================
class UserDetailView(DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    context_object_name = "user_obj"


# ================================
# ➕ CREATE USER
# ================================
class UserCreateView(CreateView):
    model = User
    fields = ["username", "email"]
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        password = self.request.POST.get("password")
        role = self.request.POST.get("role")

        user = self.object
        if password:
            user.set_password(password)
            user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        return response


# ================================
# ✏️ UPDATE USER
# ================================
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        password = self.request.POST.get("password")
        role = self.request.POST.get("role")

        user = self.object
        if password:
            user.set_password(password)
            user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        return response


# ================================
# ❌ DELETE USER
# ================================
class UserDeleteView(DeleteView):
    model = User
    template_name = "accounts/user_confirm_delete.html"
    success_url = reverse_lazy("accounts:user_list")
