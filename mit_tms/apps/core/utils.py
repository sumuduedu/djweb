# core/utils.py

from django.urls import reverse
from django.shortcuts import get_object_or_404


def get_object(model, pk):
    """
    Safe object fetch
    """
    return get_object_or_404(model, pk=pk)


def build_url(url_name, *args, **kwargs):
    """
    Safe URL builder
    """
    try:
        return reverse(url_name, args=args, kwargs=kwargs)
    except Exception:
        return "#"


def safe_getattr(obj, attr, default=None):
    """
    Safe attribute access
    """
    return getattr(obj, attr, default)


def to_dict(instance, fields=None):
    """
    Convert model instance to dict
    """
    data = {}

    if not instance:
        return data

    for field in fields or []:
        data[field] = getattr(instance, field, None)

    return data


def chunk_list(data, size):
    """
    Split list into chunks
    """
    for i in range(0, len(data), size):
        yield data[i:i + size]


def get_user_role(user):
    """
    Central role resolver using Groups
    """
    if not user.is_authenticated:
        return "GUEST"

    if user.is_superuser:
        return "ADMIN"

    if user.groups.exists():
        return user.groups.first().name.upper()

    return "GUEST"
