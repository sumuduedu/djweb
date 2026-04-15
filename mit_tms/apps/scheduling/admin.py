from django.contrib import admin

# Register your models here.
# apps/batch/admin.py
# Register your models here.
from django.contrib import admin



from .models import TimeSlot

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "end_time", "order", "is_break")
    ordering = ("order",)
