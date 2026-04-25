from django import forms
from apps.courses.models import Unit
from .base import BaseForm


class UnitForm(BaseForm):
    class Meta:
        model = Unit
        fields = [
            'ncs',
            'course',
            'code',
            'title',
            'description',
            'level',
            'order',
        ]

    def clean(self):
        cleaned_data = super().clean()

        ncs = cleaned_data.get('ncs')
        code = cleaned_data.get('code')

        if ncs and code:
            exists = Unit.objects.filter(
                ncs=ncs,
                code=code
            ).exclude(pk=self.instance.pk).exists()

            if exists:
                raise forms.ValidationError(
                    "Unit code already exists in this NCS."
                )

        return cleaned_data
