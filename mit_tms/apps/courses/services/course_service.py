from django.urls import reverse
from apps.courses.selectors.course_selector import CourseSelector


class CourseService:

    @staticmethod
    def get_table(user):
        courses = CourseSelector.list_with_related(user)

        return {
            "columns": [
                {"label": "Course", "field": "course"},
                {"label": "Level", "field": "level"},
                {"label": "NVQ", "field": "nvq"},
                {"label": "Duration", "field": "duration"},
                {"label": "Hours", "field": "hours"},
                {"label": "Fee", "field": "fee"},
                {"label": "Status", "field": "status"},
            ],
            "rows": [
                {
                    "id": c.id,

                    # 🔥 FIX: move here
                    "detail_url": reverse("courses:course_detail", args=[c.id]),

                    # 📘 Course info
                    "course": {
                        "title": c.title,
                        "code": c.code,
                    },

                    # 📊 Details
                    "level": c.get_level_display() if hasattr(c, "get_level_display") else c.level,
                    "nvq": f"NVQ {c.nvq_level}" if c.nvq_level else "-",
                    "duration": f"{c.duration_months} mo",
                    "hours": f"{c.total_hours} hrs",
                    "fee": "Free" if getattr(c, "is_free", False) else c.course_fee,

                    # 🟢 Status
                    "status": {
                        "value": c.status,
                        "label": c.get_status_display(),
                        "color": (
                            "green" if c.status == "ACTIVE"
                            else "yellow" if c.status == "DRAFT"
                            else "red"
                        ),
                    },

                    # ⚙️ Actions
                    "actions": {
                        "edit": reverse("courses:course_update", args=[c.id]),
                        "delete": reverse("courses:course_delete", args=[c.id]),
                    }
                }
                for c in courses
            ]
        }
