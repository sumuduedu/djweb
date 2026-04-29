from django.contrib import admin

# ========================
# RESOURCES
# ========================
from .models.resource import LearningResource, PhysicalResource
from .models.activity import Activity

@admin.register(PhysicalResource)
class PhysicalResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    search_fields = ("name",)
    list_filter = ("type",)


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "course")
    search_fields = ("name",)
    list_filter = ("type", "course")


# ========================
# COURSE STRUCTURE
# ========================
from apps.courses.models import Course, Module, Task


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    inlines = [ModuleInline]


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)
    search_fields = ("title",)
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "module")
    list_filter = ("module",)
    search_fields = ("title",)


# ========================
# LESSON PLAN
# ========================
from apps.lessonplan.models import LessonPlan, LessonActivity


class LessonActivityInline(admin.TabularInline):
    model = LessonActivity
    extra = 1


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "date")
    list_filter = ("task",)
    inlines = [LessonActivityInline]


@admin.register(LessonActivity)
class LessonActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "method", "total_time")
    list_filter = ("method",)


# ========================
# ELEMENT + CRITERIA
# ========================
from .models.element import Element
from .models.criteria import PerformanceCriteria


class PerformanceCriteriaInline(admin.TabularInline):
    model = PerformanceCriteria
    extra = 1


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "code", "order")
    list_filter = ("unit",)
    search_fields = ("title", "code")
    ordering = ("unit", "order")
    inlines = [PerformanceCriteriaInline]
    autocomplete_fields = ("unit",)


@admin.register(PerformanceCriteria)
class PerformanceCriteriaAdmin(admin.ModelAdmin):
    list_display = ("short_description", "element")
    search_fields = ("description",)
    list_filter = ("element",)

    def short_description(self, obj):
        return obj.description[:60]

from .models.unit import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)
    search_fields = ("title",)
from .models.standards import TaskStandard

class TaskStandardInline(admin.TabularInline):
    model = TaskStandard
    extra = 1

@admin.register(TaskStandard)
class TaskStandardAdmin(admin.ModelAdmin):
    list_display = ("short_description", "task", "order", "is_mandatory")
    list_filter = ("task", "is_mandatory")
    search_fields = ("description",)

    def short_description(self, obj):
        return obj.description[:60]

from .models.assessment import Assessment
from .models.assessment import TaskAssessment

class AssessmentInline(admin.TabularInline):
    model = Assessment
    extra = 1

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "type", "max_marks", "order")
    list_filter = ("type", "task")
    search_fields = ("title", "task__title")
    ordering = ("task", "order")




from django.contrib import admin
from .models import StudentTask


from django.contrib import admin
from .models.tracking import StudentTask


@admin.register(StudentTask)
class StudentTaskAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "task",
        "status",
        "score",
        "competency_achieved",
        "started_at",
        "completed_at"
    )

    list_filter = ("status", "competency_achieved")
    search_fields = ("student__full_name", "task__title")


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "type", "duration_minutes")
    list_filter = ("type",)
    search_fields = ("title", "task__title")

    autocomplete_fields = ("task",)
