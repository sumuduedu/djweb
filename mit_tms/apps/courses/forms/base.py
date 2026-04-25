from django import forms


from django import forms

class BaseForm(forms.ModelForm):
    """
    Apply consistent Tailwind styling to all fields
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            # Checkboxes (special styling)
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    "class": "mr-2"
                })
            else:
                field.widget.attrs.update({
                    "class": "w-full border rounded px-3 py-2"
                })

            # Optional: auto placeholder
            field.widget.attrs.setdefault("placeholder", field.label)
