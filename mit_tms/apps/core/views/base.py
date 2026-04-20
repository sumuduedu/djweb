from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from apps.accounts.models import Profile


class BaseView(LoginRequiredMixin, TemplateView):
    allowed_roles = None  # e.g. ['ADMIN'], ['STAFF']

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # 🔥 Get profile ONCE (no unnecessary writes)
        self.profile = getattr(user, "profile", None)

        if not self.profile:
            self.profile = Profile.objects.create(user=user)

        # 🔥 SUPERUSER OVERRIDE
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Normalize role
        self.role = (self.profile.role or "").upper()

        # 🔥 Role check
        if self.allowed_roles:
            allowed = [r.upper() for r in self.allowed_roles]

            if self.role not in allowed:
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    # 🔥 Helper methods (VERY USEFUL)
    def has_role(self, *roles):
        return self.role in [r.upper() for r in roles]

    def is_student(self):
        return self.role == "STUDENT"

    def is_teacher(self):
        return self.role == "TEACHER"

    def is_admin(self):
        return self.role == "ADMIN" or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "profile": self.profile,
            "role": self.role,

            # 🔥 Role flags (clean + reusable)
            "is_admin": self.is_admin(),
            "is_staff": self.has_role("STAFF"),
            "is_teacher": self.is_teacher(),
            "is_student": self.is_student(),
            "is_parent": self.has_role("PARENT"),
            "is_guest": self.has_role("GUEST"),
        })

        return context
