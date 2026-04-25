from django import forms
from django.forms import inlineformset_factory
from apps.courses.models import Unit, Element


class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['title']


ElementFormSet = inlineformset_factory(
    Unit,
    Element,
    form=ElementForm,
    extra=1,
    can_delete=True
)
