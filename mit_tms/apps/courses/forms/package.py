from django import forms
from apps.courses.models import Package


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        fields = ['ncs', 'name', 'code', 'order']

        widgets = {
            'ncs': forms.Select(attrs={
                'class': 'w-full border rounded px-3 py-2'
            }),

            'name': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Enter package name'
            }),

            'code': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Optional code'
            }),

            'order': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2'
            }),
        }

    # 🔥 Validation (important)
    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get('name')
        ncs = cleaned_data.get('ncs')

        if name and ncs:
            exists = Package.objects.filter(
                name=name,
                ncs=ncs
            ).exclude(pk=self.instance.pk).exists()

            if exists:
                raise forms.ValidationError(
                    "Package with this name already exists for this NCS."
                )

        return cleaned_data
