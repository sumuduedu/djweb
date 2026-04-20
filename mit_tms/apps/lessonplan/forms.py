# forms.py

from django import forms
from .models import LessonPlan


class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'materials': forms.Textarea(attrs={'rows': 3}),
            'competency': forms.Textarea(attrs={'rows': 3}),
        }

# forms.py

from django.forms import inlineformset_factory
from .models import LessonPlan, LessonActivity

LessonActivityFormSet = inlineformset_factory(
    LessonPlan,
    LessonActivity,
    fields=["activity_type", "description", "duration_minutes", "order"],
    extra=3,
    can_delete=True
)
