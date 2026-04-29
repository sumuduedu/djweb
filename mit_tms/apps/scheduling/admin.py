# apps/batch/admin.py

from django.contrib import admin
from .models import TimeSlot, Timetable, Session, ModulePlan


# =========================
# ⏰ TIME SLOT
# =========================
@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "end_time", "order", "is_break")
    ordering = ("order",)
    search_fields = ("name",)


# =========================
# 📅 TIMETABLE
# =========================
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = (
        "batch",
        "module",
        "day",
        "week",
        "row_slot",
        "session_type",
        "date"
    )

    list_filter = ("batch", "module", "day", "session_type")
    search_fields = ("batch__name", "module__title")

    autocomplete_fields = ("batch", "module", "slot")

    ordering = ("batch", "day", "row_slot")


# =========================
# 🎓 SESSION
# =========================
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "timetable",
        "conducted",
        "started_at",
        "ended_at"
    )

    list_filter = ("conducted",)
    search_fields = ("timetable__batch__name",)


# =========================
# 📘 MODULE PLAN
# =========================
@admin.register(ModulePlan)
class ModulePlanAdmin(admin.ModelAdmin):
    list_display = (
        "batch",
        "module",
        "start_date",
        "end_date",
        "theory_hours",
        "practical_hours"
    )

    list_filter = ("batch", "module")
    search_fields = ("module__title", "batch__name")

    autocomplete_fields = ("batch", "module")
