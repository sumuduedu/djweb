from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            "full_name",
            "bio",
            "skills",
            "education",
            "training",
            "experience",
            "cv",
            "is_public",
        ]

        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "experience": forms.Textarea(attrs={"rows": 4}),
            "education": forms.Textarea(attrs={"rows": 3}),
            "training": forms.Textarea(attrs={"rows": 3}),
        }
