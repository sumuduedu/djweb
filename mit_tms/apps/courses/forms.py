
from django import forms
from django.forms import inlineformset_factory

from .models import Course, Module, Task, Unit, Element


# =========================================================
# 🔷 COURSE FORM
# =========================================================

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'code': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'level': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'nvq_level': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'qualification_code': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'prerequisite': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'learning_outcomes': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }


# =========================================================
# 🔷 MODULE FORM
# =========================================================

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['course', 'code', 'title', 'description', 'order']

        widgets = {
            'course': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'code': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'order': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }


# =========================================================
# 🔷 TASK FORM
# =========================================================

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'duration_hours',
            'is_mandatory',
            'order'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'is_mandatory': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'order': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }


# =========================================================
# 🔥 ELEMENT FORM (DEFINE FIRST)
# =========================================================

class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Enter element title'
            }),
        }


# =========================================================
# 🔷 UNIT FORM
# =========================================================

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['code', 'title', 'description', 'level']

        widgets = {
            'code': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'level': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }


# =========================================================
# 🔥 INLINE FORMSET (OUTSIDE CLASSES)
# =========================================================

ElementFormSet = inlineformset_factory(
    Unit,
    Element,
    form=ElementForm,
    extra=2,
    can_delete=True
)
