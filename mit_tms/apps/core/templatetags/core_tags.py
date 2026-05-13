from django import template

register = template.Library()


# =========================
# 🔹 SAFE DICT ACCESS
# =========================
@register.filter(name="get_item")
def get_item(obj, key):
    """
    Safely get dictionary value by key.

    Usage:
    {{ row|get_item:"field" }}
    {{ row|get_item:col.field }}
    """
    try:
        if isinstance(obj, dict):
            return obj.get(key)
        return None
    except Exception:
        return None


# =========================
# 🔹 SAFE ATTRIBUTE ACCESS
# =========================
@register.filter(name="attr")
def attr(obj, field_name):
    """
    Safely get object attribute.

    Usage:
    {{ object|attr:"name" }}
    """
    try:
        return getattr(obj, field_name, "")
    except Exception:
        return ""


# =========================
# 🔹 DICT KEY EXISTS
# =========================
@register.filter(name="has_key")
def has_key(obj, key):
    """
    Check if dictionary has a key.

    Usage:
    {% if row|has_key:"actions" %}
    """
    try:
        return isinstance(obj, dict) and key in obj
    except Exception:
        return False


# =========================
# 🔹 DEFAULT VALUE
# =========================
@register.filter(name="default_if_none_safe")
def default_if_none_safe(value, default=""):
    """
    Safe fallback for None values.

    Usage:
    {{ value|default_if_none_safe:"-" }}
    """
    return value if value is not None else default


# =========================
# 🔹 LENGTH SAFE
# =========================
@register.filter(name="length_safe")
def length_safe(value):
    """
    Safe length check.

    Usage:
    {{ list|length_safe }}
    """
    try:
        return len(value)
    except Exception:
        return 0

# =========================
# 🔹 FORM FIELD ACCESS (IMPORTANT)
# =========================
@register.filter(name="get_field")
def get_field(form, field_name):
    if not form:
        return None

    field = form.fields.get(field_name)

    if not field:
        return None

    bound_field = form[field_name]

    # 🔥 Inject default styling
    if "class" not in bound_field.field.widget.attrs:
        bound_field.field.widget.attrs["class"] = "w-full border rounded p-2"

    return bound_field
