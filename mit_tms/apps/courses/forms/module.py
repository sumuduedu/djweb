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


        theory = cleaned_data.get('theory_hours') or 0
        practical = cleaned_data.get('practical_hours') or 0



        return cleaned_data
