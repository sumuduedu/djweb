from django.contrib import admin

from website.models.page import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "page_type",
        "is_active",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }
from django.contrib import admin

from website.models.feature import Feature


class FeatureInline(admin.TabularInline):

    model = Feature

    extra = 1
