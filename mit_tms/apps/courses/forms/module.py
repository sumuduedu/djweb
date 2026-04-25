from django import forms
from apps.courses.models import Module
from .base import BaseForm


class ModuleForm(BaseForm):
    class Meta:
        model = Module
        fields = [
            'course',
            'code',
            'title',
            'description',
            'module_type',

            'total_hours',
            'theory_hours',
            'practical_hours',

            'learning_outcomes',
            'theory_content',
            'practical_content',

            'teaching_methods',
            'assessment_methods',

            'order'
        ]

    def clean(self):
        cleaned_data = super().clean()

        total = cleaned_data.get('total_hours') or 0
        theory = cleaned_data.get('theory_hours') or 0
        practical = cleaned_data.get('practical_hours') or 0

        if total and (theory + practical) > total:
            raise forms.ValidationError(
                "Theory + Practical cannot exceed total hours."
            )

        return cleaned_data
