# apps/core/forms.py

from django import forms
from apps.enrolment.models import EnrollmentInquiry


class ApplicationForm(forms.ModelForm):

    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent'),
    )

    role_type = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = EnrollmentInquiry
        fields = [
            'phone',
            'home_phone',
            'current_address',
            'permanent_address',
            'qualification',
            'nic_number',
            'nic_copy',
            'parent_name',
            'parent_email',
            'student_name',
            'student_age',
            'relationship',
            'notes',
        ]

    # 🎨 apply styling
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "input-field"
            })

    # 🔥 validation
    def clean(self):
        cleaned_data = super().clean()
        role_type = cleaned_data.get("role_type")

        if role_type == "PARENT":
            required_fields = [
                "parent_name",
                "parent_email",
                "student_name"
            ]

            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "Required for parent application")

        return cleaned_data
