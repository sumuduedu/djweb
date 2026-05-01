from django.urls import reverse
from apps.courses.models import Course
from apps.courses.selectors.course_selector import CourseSelector


class CourseService:

    # =========================
    # 📋 LIST (TABLE)
    # =========================
    @staticmethod
    def get_table(user):
        courses = CourseSelector.list_with_related(user)

        return {
            "columns": [
                {"label": "Course", "field": "course", "type": "object"},
                {"label": "Level", "field": "level", "type": "text"},
                {"label": "NVQ", "field": "nvq", "type": "text"},
                {"label": "Duration", "field": "duration", "type": "text"},
                {"label": "Hours", "field": "hours", "type": "text"},
                {"label": "Fee", "field": "fee", "type": "text"},
                {"label": "Status", "field": "status", "type": "badge"},
                {"label": "Actions", "field": "actions", "type": "actions"},
            ],

            "rows": [CourseService._build_row(c, user) for c in courses]
        }

    # =========================
    # 🔹 BUILD ROW (CLEAN)
    # =========================
    @staticmethod
    def _build_row(c, user):
        return {
            "id": c.id,
            "detail_url": reverse("courses:course_detail", args=[c.id]),

            # 📘 Course display
            "course": {
                "title": c.title,
                "code": c.code,
            },

            # 📊 Text fields
            "level": c.get_level_display() if hasattr(c, "get_level_display") else c.level,
            "nvq": f"NVQ {c.nvq_level}" if c.nvq_level else "-",
            "duration": f"{c.duration_months} mo",
            "hours": f"{c.total_hours} hrs",
            "fee": "Free" if c.is_free else (f"LKR {c.course_fee}" if c.course_fee else "-"),

            # 🟢 Status badge
            "status": {
                "value": c.status,
                "label": c.get_status_display(),
                "color": (
                    "green" if c.status == "ACTIVE"
                    else "yellow" if c.status == "DRAFT"
                    else "red"
                ),
            },

            # ⚙️ Actions (permission-ready)
            "actions": CourseService._build_actions(c, user)
        }

    # =========================
    # 🔹 ACTION BUILDER
    # =========================
    @staticmethod
    def _build_actions(c, user):
        return [
            {
                "label": "Edit",
                "url": reverse("courses:course_update", args=[c.id]),
                "type": "edit",
                "visible": True,  # 👉 later: user.has_perm(...)
            },
            {
                "label": "Delete",
                "url": reverse("courses:course_delete", args=[c.id]),
                "type": "delete",
                "visible": True,
            }
        ]

    # =========================
    # 🔍 DETAIL
    # =========================
    @staticmethod
    def get_detail(course_id):
        course = CourseSelector.get_by_id(course_id)

        return {
            "id": course.id,
            "title": course.title,
            "code": course.code,
            "description": course.description,
            "level": course.get_level_display(),
            "nvq": course.nvq_level,
            "duration": course.duration_months,
            "hours": course.total_hours,
            "status": course.status,
        }

    # =========================
    # ➕ CREATE
    # =========================
    @staticmethod
    def create(data, user=None):
        return Course.objects.create(**data)

    # =========================
    # ✏️ UPDATE
    # =========================
    @staticmethod
    def update(course_id, data, user=None):
        course = CourseSelector.get_by_id(course_id)

        for field, value in data.items():
            setattr(course, field, value)

        course.save()
        return course

    # =========================
    # 🗑 DELETE
    # =========================
    @staticmethod
    def delete(course_id, user=None):
        course = CourseSelector.get_by_id(course_id)
        course.delete()
        return True
