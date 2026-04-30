from django import forms

class BaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    "class": "w-full px-3 py-2 border rounded-lg bg-white focus:ring-2 focus:ring-blue-500"
                })

            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": "w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500",
                    "rows": 3
                })

            else:
                field.widget.attrs.update({
                    "class": "w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                })
