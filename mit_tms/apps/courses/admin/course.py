from django.contrib import admin
from apps.courses.models import Course, Module, Task
from apps.courses.models.resource import LearningResource


# =====================================================
# 🔷 INLINE MODELS
# =====================================================

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    autocomplete_fields = ("course",)


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    autocomplete_fields = ("module",)


class LearningResourceInline(admin.TabularInline):
    model = LearningResource
    extra = 0
    autocomplete_fields = ("course",)


# =====================================================
# 🔷 COURSE ADMIN
# =====================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "code",
        "level",
        "delivery_mode",
        "course_mode",
        "status",
    )

    list_filter = (
        "level",
        "delivery_mode",
        "course_mode",
        "status",
        "medium",
    )

    search_fields = (   # 🔥 REQUIRED for autocomplete
        "title",
        "code",
        "description",
    )

    ordering = ("title",)

    inlines = [ModuleInline, LearningResourceInline]

    prepopulated_fields = {"slug": ("title",)}


# =====================================================
# 🔷 MODULE ADMIN
# =====================================================

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)

    search_fields = (   # 🔥 REQUIRED for autocomplete
        "title",
        "course__title",
    )

    ordering = ("course", "id")

    inlines = [TaskInline]

    autocomplete_fields = ("course",)


# =====================================================
# 🔷 TASK ADMIN
# =====================================================

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "module")
    list_filter = ("module",)

    search_fields = (   # 🔥 REQUIRED
        "title",
        "module__title",
    )

    ordering = ("module", "id")

    autocomplete_fields = ("module",)
