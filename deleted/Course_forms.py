
from django import forms
from django.forms import inlineformset_factory

from .models import Course, Module, Task, Unit, Element, PerformanceCriteria
from .models import Course, LearningResource
# =========================================================
# 🔷 COURSE FORM
# =========================================================

from .models import Course
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

        widgets = {
            # BASIC
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'code': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),

            # STATUS
            'active': forms.CheckboxInput(attrs={'class': 'mr-2'}),

            # ACADEMIC
            'level': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'entry_qualification': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'curriculum_category': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'curriculum_availability': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'equivalent_course': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'industry': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),

            # DELIVERY
            'delivery_mode': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'course_mode': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'medium': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),

            # DURATION
            'duration_months': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'theory_hours': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'practical_hours': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'assignment_hours': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'ojt_months': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),

            # CAPACITY
            'batches_per_year': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'students_per_batch': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),

            # FINANCIAL
            'course_fee': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'mr-2'}),
            'fee_includes': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),

            # RESOURCES
            'tools_available': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'equipment_available': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'machinery_available': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),

            # NVQ
            'nvq_level': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'qualification_code': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),

            # PEDAGOGY
            'prerequisite': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'learning_outcomes': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        theory = cleaned_data.get('theory_hours') or 0
        practical = cleaned_data.get('practical_hours') or 0
        assignment = cleaned_data.get('assignment_hours') or 0

        if theory == 0 and practical == 0 and assignment == 0:
            raise forms.ValidationError(
                "At least one duration value must be provided."
            )

        return cleaned_data
# =========================================================
# 🔷 MODULE FORM
# =========================================================
class ModuleForm(forms.ModelForm):
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

        widgets = {
            'course': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'code': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'module_type': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),

            'total_hours': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'theory_hours': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'practical_hours': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),

            'learning_outcomes': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'theory_content': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'practical_content': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),

            'teaching_methods': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'assessment_methods': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),

            'order': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }

    # ✅ CORRECT
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

    # 🔥 MUST BE OUTSIDE Meta
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')

        course = self.instance.course if hasattr(self.instance, 'course') else None

        if course and code:
            if Unit.objects.filter(course=course, code=code).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    "A unit with this code already exists for this course."
                )

        return cleaned_data

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

class PerformanceCriteriaForm(forms.ModelForm):
    class Meta:
        model = PerformanceCriteria
        fields = ['description']

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Enter performance criteria'
            })
        }


CriteriaFormSet = inlineformset_factory(
    Element,
    PerformanceCriteria,
    form=PerformanceCriteriaForm,
    extra=2,
    can_delete=True
)

from django import forms
from .models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'title',
            'description',
            'duration_minutes',
            'type',
            'order',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

from django.forms import inlineformset_factory


ResourceFormSet = inlineformset_factory(
    Course,
    LearningResource,
    fields=['name', 'type', 'file', 'url', 'description'],  # ✅ removed 'order'
    extra=1,
    can_delete=True
)
