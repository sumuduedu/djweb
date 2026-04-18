from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from apps.accounts.models import Profile


class BaseView(LoginRequiredMixin, TemplateView):
    allowed_roles = None  # e.g. ['ADMIN'], ['STAFF']

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # Ensure profile exists
        self.profile, _ = Profile.objects.get_or_create(user=user)

        # 🔥 SUPERUSER OVERRIDE (VERY IMPORTANT)
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Normalize role (avoid case issues)
        user_role = (self.profile.role or "").upper()

        # Role check
        if self.allowed_roles:
            allowed = [r.upper() for r in self.allowed_roles]

            if user_role not in allowed:
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        role = (self.profile.role or "").upper()

        context.update({
            "profile": self.profile,
            "role": role,

            # Role flags (used in sidebar/templates)
            "is_admin": role == "ADMIN" or self.request.user.is_superuser,
            "is_staff": role == "STAFF",
            "is_teacher": role == "TEACHER",
            "is_student": role == "STUDENT",
            "is_parent": role == "PARENT",
            "is_guest": role == "GUEST",
        })

        return context
