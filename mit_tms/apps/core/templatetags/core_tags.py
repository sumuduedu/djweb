from django import template

register = template.Library()


@register.filter
def get_item(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return None


@register.filter
def attr(obj, field_name):
    return getattr(obj, field_name, "")
