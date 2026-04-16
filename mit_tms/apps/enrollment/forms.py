# apps/core/forms.py

from django import forms
from apps.enrolment.models import EnrollmentInquiry

class StudentApplicationForm(forms.ModelForm):

    class Meta:
        model = EnrollmentInquiry
        fields = [
            'phone',
            'address',
            'qualification',
            'notes'
        ]
