from django import forms
from apps.courses.models import Course
from .base import BaseForm


class CourseForm(BaseForm):

    class Meta:
        model = Course

        # 🔥 Explicit fields (better than '__all__')
        fields = [
            "title", "code", "description", "status",

            "level", "entry_qualification", "medium",
            "curriculum_category", "curriculum_availability",
            "equivalent_course", "industry",

            "delivery_mode", "course_mode",

            "duration_months", "theory_hours",
            "practical_hours", "assignment_hours", "ojt_months",

            "batches_per_year", "students_per_batch",

            "course_fee", "is_free", "fee_includes",

            "physical_resources",
            "tools_available", "equipment_available", "machinery_available",

            "nvq_level", "qualification_code",

            "prerequisite", "learning_outcomes",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "tools_available": forms.Textarea(attrs={"rows": 3}),
            "equipment_available": forms.Textarea(attrs={"rows": 3}),
            "machinery_available": forms.Textarea(attrs={"rows": 3}),
            "learning_outcomes": forms.Textarea(attrs={"rows": 4}),
            "prerequisite": forms.Textarea(attrs={"rows": 3}),
        }

        labels = {
            "course_fee": "Course Fee (LKR)",
            "ojt_months": "OJT Duration (Months)",
        }

        help_texts = {
            "learning_outcomes": "Write outcomes as bullet points",
        }

    # =========================
    # 🔍 VALIDATION
    # =========================
    def clean(self):
        cleaned_data = super().clean()

        theory = cleaned_data.get('theory_hours') or 0
        practical = cleaned_data.get('practical_hours') or 0
        assignment = cleaned_data.get('assignment_hours') or 0

        if theory == 0 and practical == 0 and assignment == 0:
            raise forms.ValidationError(
                "At least one duration value must be provided."
            )

        return cleaned_data
