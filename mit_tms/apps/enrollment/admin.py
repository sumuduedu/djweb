from django.contrib import admin
from django.contrib import admin
from .models import EnrollmentInquiry
# Register your models here.
# admin.py
from django.contrib import admin
from .models import EnrollmentInquiry, Enrollment


@admin.register(EnrollmentInquiry)
class EnrollmentInquiryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'course',
        'status',
        'current_stage',
        'risk_score',
        'is_flagged',
    )

    list_filter = ('status', 'current_stage')
    search_fields = ('full_name', 'email', 'course__title')

    list_editable = ('status', 'current_stage')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'batch', 'status', 'enrolled_at')
