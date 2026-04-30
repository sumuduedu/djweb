from django import template

register = template.Library()


@register.inclusion_tag("components/auto_field.html")
def render_field(form, field_name):
    try:
        field = form[field_name]
    except KeyError:
        return {
            "field": None,
            "label": f"Field '{field_name}' NOT FOUND ❌",
            "widget_type": None,
        }

    return {
        "field": field,
        "label": field.label,
        "widget_type": field.field.widget.__class__.__name__,
    }
