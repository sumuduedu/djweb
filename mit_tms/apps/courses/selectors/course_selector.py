# courses/selectors/course_selector.py

from django.db.models import Count, Q
from courses.models import Course

class CourseSelector:

    @staticmethod
    def list(user):
        queryset = Course.objects.all()

        # 🔒 Row-level security
        if user.groups.filter(name="Student").exists():
            queryset = queryset.filter(enrollments__student=user.student)

        elif user.groups.filter(name="Teacher").exists():
            queryset = queryset.filter(modules__teacher=user.teacher)

        return queryset.distinct()

    @staticmethod
    def get_by_id(course_id):
        return Course.objects.get(id=course_id)

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
        queryset = CourseSelector.list(user)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(code__icontains=query)
            )

        if filters:
            if filters.get("level"):
                queryset = queryset.filter(level=filters["level"])

            if filters.get("status"):
                queryset = queryset.filter(status=filters["status"])

        return queryset

    @staticmethod
    def stats():
        return Course.objects.aggregate(
            total_courses=Count("id"),
            active_courses=Count("id", filter=Q(status="ACTIVE"))
        )

    @staticmethod
    def simple_list():
        return Course.objects.values("id", "title", "code")
