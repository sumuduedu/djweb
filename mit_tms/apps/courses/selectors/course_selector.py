from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from ..models import Course


class CourseSelector:

    # =========================
    # 🔐 ROLE FILTER BASE
    # =========================
    @staticmethod
    def base_queryset(user):
        qs = Course.objects.all()

        if user.is_superuser:
            return qs

        # Student
        if hasattr(user, "student"):
            qs = qs.filter(enrollments__student=user.student)

        # Teacher
        elif hasattr(user, "teacher"):
            qs = qs.filter(modules__teacher=user.teacher)

        return qs.distinct()

    # =========================
    # 📋 LIST
    # =========================
    @staticmethod
    def list(user):
        return CourseSelector.base_queryset(user).order_by("-created_at")

    # =========================
    # 🔍 GET BY ID (FOR DETAIL / UPDATE / DELETE)
    # =========================
    @staticmethod
    def get_by_id(course_id, user=None):
        qs = Course.objects.all()

        # Optional: enforce row-level security
        if user:
            qs = CourseSelector.base_queryset(user)

        return get_object_or_404(qs, id=course_id)

    # =========================
    # ⚡ LIST WITH RELATED (FOR UI / TABLE)
    # =========================
    @staticmethod
    def list_with_related(user):
        qs = CourseSelector.base_queryset(user)

        return qs.select_related("ncs").prefetch_related(
            "modules",
            "modules__tasks",
            "resources",
            "physical_resources"
        ).annotate(
            enrolled_count=Count("enrollments", distinct=True),
            module_count=Count("modules", distinct=True),
            task_count=Count("modules__tasks", distinct=True),
        ).order_by("-created_at")

    # =========================
    # 🔎 SEARCH + FILTER
    # =========================
    @staticmethod
    def search(user, query=None, filters=None):
        filters = filters or {}
        qs = CourseSelector.list_with_related(user)

        # 🔍 Search
        if query:
            query = query.strip()
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(code__icontains=query)
            )

        # 🎯 Filters
        if filters.get("level"):
            qs = qs.filter(level=filters["level"])

        if filters.get("status"):
            qs = qs.filter(status=filters["status"])

        if filters.get("nvq_level"):
            qs = qs.filter(nvq_level=filters["nvq_level"])

        if filters.get("is_free") is not None:
            qs = qs.filter(is_free=filters["is_free"])

        return qs

    # =========================
    # 📊 STATS (FOR CARDS)
    # =========================
    @staticmethod
    def stats(user):
        qs = CourseSelector.base_queryset(user)

        return qs.aggregate(
            total_courses=Count("id"),
            active_courses=Count("id", filter=Q(status="ACTIVE")),
            draft_courses=Count("id", filter=Q(status="DRAFT")),
            total_enrollments=Count("enrollments", distinct=True),
        )

    # =========================
    # 📦 SIMPLE LIST (FOR DROPDOWN/API)
    # =========================
    @staticmethod
    def simple_list(user=None):
        qs = Course.objects.all()

        if user:
            qs = CourseSelector.base_queryset(user)

        return qs.values("id", "title", "code", "level")
