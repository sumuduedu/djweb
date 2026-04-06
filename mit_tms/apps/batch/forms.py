from django import forms
from .models import Batch, Timetable, ModulePlan


# =========================================================
# 🔷 BATCH FORM
# =========================================================

class BatchForm(forms.ModelForm):

    class Meta:
        model = Batch
        fields = [
            'course',
            'academic_year',
            'name',
            'start_date',
            'hours_per_day',
            'days_per_week',
            'max_students',
        ]

        widgets = {
            'course': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'academic_year': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),

            'name': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),

            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border rounded px-3 py-2'
            }),

            'hours_per_day': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.5'
            }),

            'days_per_week': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'min': 1,
                'max': 7
            }),

            'max_students': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2'
            }),
        }

    # 🔥 VALIDATION
    def clean(self):
        cleaned_data = super().clean()

        hours_per_day = cleaned_data.get('hours_per_day')
        days_per_week = cleaned_data.get('days_per_week')

        if hours_per_day and hours_per_day <= 0:
            raise forms.ValidationError("Hours per day must be greater than 0.")

        if days_per_week and not (1 <= days_per_week <= 7):
            raise forms.ValidationError("Days per week must be between 1 and 7.")

        return cleaned_data


# =========================================================
# 🔷 TIMETABLE FORM (MATCHES YOUR MODEL)
# =========================================================

class TimetableForm(forms.ModelForm):

    class Meta:
        model = Timetable
        fields = [
            'module',
            'week',
            'day',
            'row_slot',
        ]

        widgets = {
            'module': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),

            'week': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'min': 1
            }),

            'day': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'min': 1,
                'max': 7
            }),

            'row_slot': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'min': 1
            }),
        }


# =========================================================
# 🔷 MODULE PLAN FORM (SMART FILTER 🔥)
# =========================================================

class ModulePlanForm(forms.ModelForm):

    class Meta:
        model = ModulePlan
        fields = [
            'module',
            'start_date',
            'end_date',
            'theory_hours',
            'practical_hours'
        ]

        widgets = {
            'module': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),

            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border rounded px-3 py-2'
            }),

            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border rounded px-3 py-2'
            }),

            'theory_hours': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.5'
            }),

            'practical_hours': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.5'
            }),
        }

    # 🔥 FILTER MODULES BASED ON BATCH (IMPORTANT)
    def __init__(self, *args, **kwargs):
        batch = kwargs.pop('batch', None)
        super().__init__(*args, **kwargs)

        if batch:
            self.fields['module'].queryset = batch.course.modules.all()

    # 🔥 VALIDATION
    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and end and start > end:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data
