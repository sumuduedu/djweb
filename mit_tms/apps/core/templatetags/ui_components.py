from django import template

register = template.Library()


# ================================
# 🔷 TABLE COMPONENT
# ================================
@register.inclusion_tag('components/table.html')
def render_table(objects, fields, entity=None):
    rows = []

    for obj in objects:
        rows.append({
            "values": [getattr(obj, f) for f in fields],
            "id": obj.id,
            "entity": entity
        })

    return {
        "columns": fields,
        "rows": rows,
        "entity": entity
    }


# ================================
# 🔷 MODEL AUTO TABLE
# ================================
@register.inclusion_tag('components/table.html')
def render_model_table(queryset, entity=None):
    fields = [f.name for f in queryset.model._meta.fields]

    rows = []
    for obj in queryset:
        rows.append({
            "values": [getattr(obj, f) for f in fields],
            "id": obj.id,
            "entity": entity
        })

    return {
        "columns": fields,
        "rows": rows,
        "entity": entity
    }


# ================================
# 🔷 CARD COMPONENT (ADVANCED)
# ================================
@register.inclusion_tag('components/card.html')
def render_card(
    title,
    value,
    subtitle=None,
    icon=None,
    extra=None,
    color="default",
    url=None
):

    COLORS = {
        "default": ("bg-white", "text-gray-500", "text-gray-800"),
        "success": ("bg-green-100", "text-green-700", "text-green-900"),
        "warning": ("bg-yellow-100", "text-yellow-700", "text-yellow-900"),
        "danger": ("bg-red-100", "text-red-700", "text-red-900"),
        "info": ("bg-blue-100", "text-blue-700", "text-blue-900"),
    }

    bg, text, value_color = COLORS.get(color, COLORS["default"])

    return {
        "title": title,
        "value": value,
        "subtitle": subtitle,
        "icon": icon,
        "extra": extra,
        "bg_color": bg,
        "text_color": text,
        "value_color": value_color,
        "clickable": url is not None,
        "url": url
    }


# ================================
# 🔷 BUTTON
# ================================
@register.inclusion_tag('components/button.html')
def render_button(url, label, color="bg-blue-600"):
    return {
        "url": url,
        "label": label,
        "color": color
    }


# ================================
# 🔷 FORM
# ================================
@register.inclusion_tag('components/form.html')
def render_form(form, cancel_url):
    return {
        "form": form,
        "cancel_url": cancel_url
    }


# ================================
# 🔷 BADGE
# ================================
@register.inclusion_tag('components/badge.html')
def render_badge(label, color="gray"):
    return {
        "label": label,
        "color": color
    }


# ================================
# 🔷 PROGRESS BAR
# ================================
@register.inclusion_tag('components/progress.html')
def render_progress(value):
    return {
        "value": value
    }


# ================================
# 🔷 ALERT
# ================================
@register.inclusion_tag('components/alert.html')
def render_alert(message, type="success"):

    COLORS = {
        "success": "bg-green-100 text-green-800",
        "error": "bg-red-100 text-red-800",
        "warning": "bg-yellow-100 text-yellow-800",
        "info": "bg-blue-100 text-blue-800",
    }

    return {
        "message": message,
        "classes": COLORS.get(type, COLORS["success"])
    }

# ================================
# 🔷 EMPTY STATE
# ================================
@register.inclusion_tag('components/empty.html')
def render_empty(message="No data available"):
    return {
        "message": message
    }


# ================================
# 🔷 CHART CARD
# ================================
@register.inclusion_tag('components/chart_card.html')
def render_chart_card(title, value, labels, data, chart_id, icon=None):
    return {
        "title": title,
        "value": value,
        "labels": labels,
        "data": data,
        "chart_id": chart_id,
        "icon": icon
    }
