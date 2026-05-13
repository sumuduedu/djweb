from django import forms
from apps.courses.models import Unit
from .base import BaseForm


class UnitForm(BaseForm):
    class Meta:
        model = Unit
        fields = [
            'package',      # ✅ changed (was ncs)
            'code',
            'title',
            'descriptor',   # ✅ changed (was description)
            'level',
            'order',
        ]

    def clean(self):
        cleaned_data = super().clean()

        package = cleaned_data.get('package')
        code = cleaned_data.get('code')

        if package and code:
            exists = Unit.objects.filter(
                package=package,
                code=code
            ).exclude(pk=self.instance.pk).exists()

            if exists:
                raise forms.ValidationError(
                    "Unit code already exists in this Package."
                )

        return cleaned_data
