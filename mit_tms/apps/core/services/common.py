# core/services/common.py

from typing import Dict, Any, Type, Optional
from django.db import transaction
from django.forms import ModelForm


# =========================
# 🔹 STANDARD RESULT
# =========================
class ServiceResult:
    def __init__(self, success: bool, instance=None, errors=None, message=None):
        self.success = success
        self.instance = instance
        self.errors = errors or {}
        self.message = message

    def to_dict(self):
        return {
            "success": self.success,
            "errors": self.errors,
            "message": self.message,
            "id": getattr(self.instance, "id", None),
        }


# =========================
# 🔹 CREATE
# =========================
@transaction.atomic
def create_instance(
    form_class: Type[ModelForm],
    data: Dict[str, Any],
    files=None,
    user=None,
) -> ServiceResult:

    form = form_class(data, files)

    if not form.is_valid():
        return ServiceResult(False, errors=form.errors, message="Validation failed")

    instance = form.save()

    return ServiceResult(True, instance=instance, message="Created successfully")


# =========================
# 🔹 UPDATE
# =========================
@transaction.atomic
def update_instance(
    form_class: Type[ModelForm],
    instance,
    data: Dict[str, Any],
    files=None,
    user=None,
) -> ServiceResult:

    form = form_class(data, files, instance=instance)

    if not form.is_valid():
        return ServiceResult(False, errors=form.errors, message="Validation failed")

    instance = form.save()

    return ServiceResult(True, instance=instance, message="Updated successfully")


# =========================
# 🔹 DELETE
# =========================
@transaction.atomic
def delete_instance(instance, user=None) -> ServiceResult:

    if not instance:
        return ServiceResult(False, message="Object not found")

    obj_id = instance.id
    instance.delete()

    return ServiceResult(True, message=f"Deleted (id={obj_id})")


# =========================
# 🔹 BULK DELETE
# =========================
@transaction.atomic
def bulk_delete(model, ids: list, user=None) -> ServiceResult:

    if not ids:
        return ServiceResult(False, message="No items selected")

    deleted_count, _ = model.objects.filter(id__in=ids).delete()

    return ServiceResult(True, message=f"{deleted_count} records deleted")
