from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.core.models import PermissionRule

@admin.register(PermissionRule)
class PermissionRuleAdmin(admin.ModelAdmin):
    list_display = ("group", "entity", "action", "allowed")
    list_filter = ("group", "entity", "action")
