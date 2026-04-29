# forms/activity.py

from django import forms
from apps.courses.models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            "title",
            "description",
            "code",
            "type",
            "duration_minutes",
            "domain",
            "bloom_level",
            "is_active",
        ]
        widgets = {
            "type": forms.Select(attrs={"id": "activity_type", "class": "input"}),
            "domain": forms.Select(attrs={"id": "domain", "class": "input"}),
            "bloom_level": forms.Select(attrs={"id": "bloom", "class": "input"}),
            "title": forms.TextInput(attrs={"class": "input"}),
            "description": forms.Textarea(attrs={"class": "input"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "input"}),
        }
