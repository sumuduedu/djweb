from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from ..models import Course


class CourseSelector:

    @staticmethod
    def list(user):
        queryset = Course.objects.all()

        # 🔥 ADD THIS
        if user.is_superuser:
            return queryset.order_by("-created_at")

        if user.groups.filter(name__iexact="student").exists() and hasattr(user, "student"):
            queryset = queryset.filter(enrollments__student=user.student)

        elif user.groups.filter(name__iexact="teacher").exists() and hasattr(user, "teacher"):
            queryset = queryset.filter(modules__teacher=user.teacher)

        return queryset.distinct().order_by("-created_at")

    @staticmethod
    def get_by_id(course_id):
        return get_object_or_404(Course, id=course_id)

    @staticmethod
    def list_with_related(user):
        queryset = CourseSelector.list(user)

        return queryset.select_related("ncs").prefetch_related(
            "modules",
            "resources",
            "physical_resources"
        )

    @staticmethod
    def search(user, query=None, filters=None):
        filters = filters or {}

        queryset = CourseSelector.list_with_related(user)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(code__icontains=query)
            )

        if filters.get("level"):
            queryset = queryset.filter(level=filters["level"])

        if filters.get("status"):
            queryset = queryset.filter(status=filters["status"])

        return queryset

    @staticmethod
    def stats(user):
        queryset = CourseSelector.list(user)

        return queryset.aggregate(
            total_courses=Count("id"),
            active_courses=Count("id", filter=Q(status="ACTIVE"))
        )

    @staticmethod
    def simple_list():
        return Course.objects.values("id", "title", "code")
