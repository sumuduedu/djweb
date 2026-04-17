from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from apps.accounts.models import Profile


class BaseView(LoginRequiredMixin, TemplateView):
    allowed_roles = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, _ = Profile.objects.get_or_create(user=request.user)

        if self.allowed_roles and self.profile.role not in self.allowed_roles:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = self.profile
        context["role"] = self.profile.role

        context["is_admin"] = self.profile.role == "ADMIN"
        context["is_staff"] = self.profile.role == "STAFF"
        context["is_teacher"] = self.profile.role == "TEACHER"
        context["is_student"] = self.profile.role == "STUDENT"
        context["is_parent"] = self.profile.role == "PARENT"
        context["is_guest"] = self.profile.role == "GUEST"

        return context
