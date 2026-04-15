from django import forms
from django.core.exceptions import ValidationError

from .models import Batch
from apps.accounts.models import Teacher


# =========================================================
# 🔷 BATCH FORM
# =========================================================
class BatchForm(forms.ModelForm):

    class Meta:
        model = Batch
        fields = [
            'course',
            'name',
            'teacher',
            'start_date',
            'end_date',
            'capacity',
        ]

        widgets = {
            'course': forms.Select(attrs={
                'class': 'w-full border rounded px-3 py-2'
            }),

            'name': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Batch Name (e.g., 2026 Morning Batch)'
            }),

            'teacher': forms.Select(attrs={
                'class': 'w-full border rounded px-3 py-2'
            }),

            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border rounded px-3 py-2'
            }),

            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border rounded px-3 py-2'
            }),

            'capacity': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'min': 1
            }),
        }

    # =========================================================
    # 🔥 INIT (FILTER TEACHERS ONLY)
    # =========================================================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only valid teachers
        self.fields['teacher'].queryset = Teacher.objects.select_related('user')

    # =========================================================
    # 🔥 VALIDATION
    # =========================================================
    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        capacity = cleaned_data.get('capacity')

        # ✅ Date validation
        if start and end and start > end:
            raise ValidationError("End date must be after start date.")

        # ✅ Capacity validation
        if capacity is not None and capacity < 1:
            raise ValidationError("Capacity must be at least 1.")

        return cleaned_data
