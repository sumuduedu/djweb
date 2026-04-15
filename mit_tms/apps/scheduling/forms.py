# =========================================================
# 🔷 IMPORTS (FIXED ORDER ✅)
# =========================================================
from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from apps.batch.models import Batch
from .models import Timetable, ModulePlan


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

        if hours_per_day is not None and hours_per_day <= 0:
            raise ValidationError("Hours per day must be greater than 0.")

        if days_per_week is not None and not (1 <= days_per_week <= 7):
            raise ValidationError("Days per week must be between 1 and 7.")

        return cleaned_data


# =========================================================
# 🔷 TIMETABLE FORM (WITH CONFLICT VALIDATION 🔥)
# =========================================================
class TimetableForm(forms.ModelForm):

    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'w-full border rounded px-3 py-2',
            }
        )
    )

    class Meta:
        model = Timetable
        fields = [
            'batch',
            'module',
            'date',
            'slot',
            'session_type',
        ]

        widgets = {
            'batch': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'module': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'slot': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'session_type': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable past dates
        self.fields['date'].widget.attrs['min'] = date.today().isoformat()

    def clean(self):
        cleaned_data = super().clean()

        batch = cleaned_data.get('batch')
        date_value = cleaned_data.get('date')
        slot = cleaned_data.get('slot')

        if batch and date_value and slot:
            qs = Timetable.objects.filter(
                batch=batch,
                date=date_value,
                slot=slot
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError(
                    "⚠️ Conflict: This batch already has a session in this time slot."
                )

        return cleaned_data


# =========================================================
# 🔷 MODULE PLAN FORM
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
            'module': forms.Select(attrs={
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

            'theory_hours': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.5'
            }),

            'practical_hours': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.5'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.batch = kwargs.pop('batch', None)
        super().__init__(*args, **kwargs)

        if self.batch and self.batch.course:
            self.fields['module'].queryset = self.batch.course.modules.all()
        else:
            self.fields['module'].queryset = self.fields['module'].queryset.none()

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        module = cleaned_data.get('module')

        if start and end and start > end:
            raise ValidationError("End date must be after start date.")

        if self.batch and module:
            if module.course != self.batch.course:
                raise ValidationError("Selected module does not belong to this batch course.")

        return cleaned_data
