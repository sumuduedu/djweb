from django import forms
from apps.courses.models import NCS


class NCSForm(forms.ModelForm):

    class Meta:
        model = NCS
        fields = ['name', 'code', 'level', 'sector', 'version', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Enter NCS name'
            }),

            'code': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Enter NCS code'
            }),

            'level': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2'
            }),

            'sector': forms.Select(attrs={
                'class': 'w-full border rounded px-3 py-2'
            }),

            'version': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'e.g. v1.0'
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'mr-2'
            }),
        }

    # 🔥 Validation
    def clean(self):
        cleaned_data = super().clean()

        code = cleaned_data.get('code')
        version = cleaned_data.get('version')

        # Unique code + version
        if code and version:
            exists = NCS.objects.filter(
                code=code,
                version=version
            ).exclude(pk=self.instance.pk).exists()

            if exists:
                raise forms.ValidationError(
                    "This NCS code + version already exists."
                )

        return cleaned_data
