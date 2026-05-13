from django.contrib import admin
from .models import *


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'duration_minutes', 'status']
    search_fields = ['title', 'subject']
    list_filter = ['status', 'level']


@admin.register(LearningOutcome)
class LearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'description']


@admin.register(LessonActivity)
class LessonActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'method', 'total_time']
    list_filter = ['method']


@admin.register(LessonSession)
class LessonSessionAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'batch', 'date', 'status']
    list_filter = ['status', 'date']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status']
    list_filter = ['status']


@admin.register(LessonPerformance)
class LessonPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'session',
        'understanding_level',
        'participation_score',
        'score'
    ]
