from django import forms
from apps.courses.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
