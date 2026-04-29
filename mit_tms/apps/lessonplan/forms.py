from django import forms
from django.forms import inlineformset_factory
from apps.courses.models import Module, Task
from .models import LessonPlan, LessonActivity

class LessonPlanForm(forms.ModelForm):

    module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        required=True,
        empty_label="Select Module"
    )

    class Meta:
        model = LessonPlan
        exclude = ['subject']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'materials': forms.Textarea(attrs={'rows': 3}),
            'competency': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['task'].queryset = Task.objects.all()
        self.fields['task'].required = True
        self.fields['task'].empty_label = "Select Module First"

        if 'module' in self.data:
            try:
                module_id = int(self.data.get('module'))
                self.fields['task'].queryset = Task.objects.filter(module_id=module_id)
            except (ValueError, TypeError):
                pass

        elif self.instance.pk and self.instance.task:
            self.fields['module'].initial = self.instance.task.module
            self.fields['task'].queryset = Task.objects.filter(module=self.instance.task.module)

    def clean(self):
        cleaned_data = super().clean()

        module = cleaned_data.get("module")
        task = cleaned_data.get("task")

        if task and module:
            if task.module != module:
                raise forms.ValidationError("Selected task does not belong to the selected module.")

        return cleaned_data


LessonActivityFormSet = inlineformset_factory(
    LessonPlan,
    LessonActivity,
    fields=[
        "title",
        "description",
        "trainer_activity",
        "trainee_activity",
        "method",
        "learning_resources",     # ✅ NEW
        "physical_resources",     # ✅ NEW

        "trainer_time",
        "trainee_time",
        "order"
    ],
    extra=3,
    can_delete=True
)



