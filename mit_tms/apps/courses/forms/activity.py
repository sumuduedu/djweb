# forms/activity.py

from django import forms
from apps.courses.models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
