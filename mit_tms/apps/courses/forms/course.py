from django import forms
from apps.courses.models import Course


from .base import BaseForm
from apps.courses.models import Course
from django import forms


class CourseForm(BaseForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        theory = cleaned_data.get('theory_hours') or 0
        practical = cleaned_data.get('practical_hours') or 0
        assignment = cleaned_data.get('assignment_hours') or 0

        if theory == 0 and practical == 0 and assignment == 0:
            raise forms.ValidationError(
                "At least one duration value must be provided."
            )
        widgets = {
                    "description": forms.Textarea(attrs={"rows": 4}),
                    "tools_available": forms.Textarea(attrs={"rows": 3}),
                }
        return cleaned_data
