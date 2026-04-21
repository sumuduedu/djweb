from django.contrib import admin
from .models import Company, Job, Application


# =========================
# 🏢 COMPANY ADMIN
# =========================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "website", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


# =========================
# 💼 JOB ADMIN
# =========================
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "job_type", "location", "is_active", "deadline")
    search_fields = ("title", "company__name", "location")
    list_filter = ("job_type", "is_active", "deadline")
    ordering = ("-created_at",)
    list_editable = ("is_active",)

    # nice grouping in form
    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "company", "description")
        }),
        ("Details", {
            "fields": ("location", "job_type", "salary", "deadline")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
    )


# =========================
# 📄 APPLICATION ADMIN
# =========================
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "status", "applied_at")
    search_fields = ("user__username", "job__title")
    list_filter = ("status", "applied_at")
    ordering = ("-applied_at",)
    list_editable = ("status",)

    # helpful optimization
    autocomplete_fields = ("user", "job")
