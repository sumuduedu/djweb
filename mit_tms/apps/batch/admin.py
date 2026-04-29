# apps/academic/admin.py  (or your app)

from django.contrib import admin
from .models import AcademicYear, Batch


# =========================
# 📅 ACADEMIC YEAR
# =========================
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name",)
    list_filter = ("start_date", "end_date")
    ordering = ("-start_date",)

    fieldsets = (
        ("Academic Year Info", {
            "fields": ("name", "start_date", "end_date")
        }),
    )


# =========================
# 🎓 BATCH
# =========================
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "course",
        "teacher",
        "start_date",
        "end_date",
        "capacity",
        "available_slots"
    )

    search_fields = ("name", "course__title", "teacher__name")
    list_filter = ("course", "teacher", "start_date")
    ordering = ("-start_date",)

    autocomplete_fields = ("course", "teacher")

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "course", "teacher")
        }),
        ("Schedule", {
            "fields": ("start_date", "end_date")
        }),
        ("Capacity", {
            "fields": ("capacity",)
        }),
    )

    # 🔥 BONUS: show available slots
    def available_slots(self, obj):
        if hasattr(obj, "students"):
            return obj.capacity - obj.students.count()
        return obj.capacity

    available_slots.short_description = "Available Slots"
