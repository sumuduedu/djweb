# core/audit.py

from django.forms.models import model_to_dict
from core.models import AuditLog


def get_changes(old_instance, new_instance):
    """
    Compare old vs new instance and return changed fields
    """
    if not old_instance:
        return {"created": model_to_dict(new_instance)}

    old_data = model_to_dict(old_instance)
    new_data = model_to_dict(new_instance)

    changes = {}

    for field in new_data:
        old_value = old_data.get(field)
        new_value = new_data.get(field)

        if old_value != new_value:
            changes[field] = {
                "old": old_value,
                "new": new_value
            }

    return changes


def log_action(user, action, instance, changes=None):
    """
    Generic audit logger
    """
    AuditLog.objects.create(
        user=user if user.is_authenticated else None,
        action=action,
        entity=instance.__class__.__name__,
        object_id=str(instance.pk),
        changes=changes or {},
    )


def log_create(user, instance):
    changes = get_changes(None, instance)
    log_action(user, "create", instance, changes)


def log_update(user, old_instance, new_instance):
    changes = get_changes(old_instance, new_instance)
    log_action(user, "update", new_instance, changes)


def log_delete(user, instance):
    changes = {"deleted": model_to_dict(instance)}
    log_action(user, "delete", instance, changes)
