
# core/permission_engine.py
class PermissionEngine:

    @staticmethod
    def get_role(user):
        if not user.is_authenticated: return "GUEST"
        if user.is_superuser: return "ADMIN"
        if hasattr(user, "staff"): return "STAFF"
        if hasattr(user, "teacher"): return "TEACHER"
        if hasattr(user, "student"): return "STUDENT"
        return "GUEST"

    @staticmethod
    def can(user, entity, action):
        role = PermissionEngine.get_role(user)
        return action in PERMISSIONS.get(entity, {}).get(role, [])

from apps.core.models import PermissionRule

class PermissionEngine:

    @staticmethod
    def get_groups(user):
        return user.groups.all()

    @staticmethod
    def can(user, entity, action):
        if not user.is_authenticated:
            return False

        return PermissionRule.objects.filter(
            group__in=user.groups.all(),
            entity=entity,
            action=action,
            allowed=True
        ).exists()
