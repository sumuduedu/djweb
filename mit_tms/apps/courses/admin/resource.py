from django.contrib import admin
from apps.courses.models import (
    Resource,
    Reference,
    Domain,
)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "unit")
    list_filter = ("type",)
    search_fields = ("name",)
    autocomplete_fields = ("unit",)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("unit", "short_description")
    search_fields = ("description",)
    autocomplete_fields = ("unit",)

    def short_description(self, obj):
        return obj.description[:50]

