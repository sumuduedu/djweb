from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


# =====================================================
# 🔷 HELPER FUNCTION
# =====================================================
def get_user_role(user):
    """
    Safely get user role from profile.
    Returns None if not available.
    """
    if not user.is_authenticated:
        return None

    return getattr(getattr(user, "profile", None), "role", None)


# =====================================================
# 🔷 ROLE REQUIRED MIXIN (MAIN PERMISSION CONTROL)
# =====================================================
class RoleRequiredMixin(UserPassesTestMixin):
    """
    Use this to restrict access based on roles.
    Example:
        allowed_roles = ["ADMIN", "STAFF"]
    """
    allowed_roles = []

    def test_func(self):
        role = get_user_role(self.request.user)
        return role in self.allowed_roles

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")


# =====================================================
# 🔷 ADMIN ONLY MIXIN (OPTIONAL SHORTCUT)
# =====================================================
class AdminRequiredMixin(RoleRequiredMixin):
    """
    Shortcut for admin-only views
    """
    allowed_roles = ["ADMIN"]


# =====================================================
# 🔷 ROLE FILTER MIXIN (DATA-LEVEL PERMISSIONS)
# =====================================================
class RoleFilterMixin:
    """
    Filters queryset based on user role.

    Requires:
    - Batch model with `instructor`
    - Enrollment model with `student` and `batch`
    """

    def filter_queryset(self, queryset):
        user = self.request.user
        role = get_user_role(user)

        # 🔓 Admin & Staff → full access
        if role in ["ADMIN", "STAFF"]:
            return queryset

        # 👨‍🏫 Teacher → only their batches
        elif role == "TEACHER":
            return queryset.filter(
                batch__instructor=user
            ).distinct()

        # 👨‍🎓 Student → enrolled courses only
        elif role == "STUDENT":
            return queryset.filter(
                batch__enrollments__student=user
            ).distinct()

        # 👪 Parent / 🎓 Alumni → read-only (adjust later if needed)
        elif role in ["PARENT", "ALUMNI"]:
            return queryset

        # ❌ No role / unknown → no access
        return queryset.none()

# core/mixins.py
from django.http import HttpResponseForbidden
from core.permission_engine import PermissionEngine

class PermissionRequiredMixin:
    entity = None     # "module", "course", ...
    action = None     # "create", "read", "update", "delete"

    def dispatch(self, request, *args, **kwargs):
        if not PermissionEngine.can(request.user, self.entity, self.action):
            return HttpResponseForbidden("Not allowed")
        return super().dispatch(request, *args, **kwargs)
