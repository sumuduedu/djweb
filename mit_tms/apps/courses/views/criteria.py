from django.urls import reverse_lazy

from .base import (
    BaseChildCreateView,
    BaseChildUpdateView,
    BaseChildDeleteView,
    BaseChildDetailView,
    BaseDetailView,
)
from django.urls import reverse_lazy
from .base import BaseChildUpdateView, BaseChildDeleteView
from ..models import PerformanceCriteria
from ..models import Element, PerformanceCriteria

class ElementCreateView(BaseChildCreateView):
    model = Element
    fields = ['title']
    template_name = "courses/elements/form.html"

    parent_field = "unit"
    parent_url_kwarg = "unit_id"

    success_message = "Element created successfully ✅"

    def get_success_url(self):
        return reverse_lazy('courses:unit_detail', kwargs={
            'pk': self.object.unit.pk
        })

class ElementDetailView(BaseDetailView):
    model = Element
    template_name = "courses/element/detail.html"
    context_object_name = "element"

    def get_extra_context(self):
        return {
            "criteria_list": self.object.criteria.all()
        }

class ElementUpdateView(BaseChildUpdateView):
    model = Element
    fields = ['title']
    template_name = "courses/element/form.html"

    parent_field = "unit"
    parent_url_kwarg = "unit_id"

    success_message = "Element updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:unit_detail', kwargs={
            'pk': self.object.unit.pk
        })
class ElementDeleteView(BaseChildDeleteView):
    model = Element
    template_name = "courses/element/confirm_delete.html"

    parent_field = "unit"
    parent_url_kwarg = "unit_id"

    success_message = "Element deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:unit_detail', kwargs={
            'pk': self.object.unit.pk
        })

class CriteriaCreateView(BaseChildCreateView):
    model = PerformanceCriteria
    fields = ['description']
    template_name = "courses/criteria_form.html"

    parent_field = "element"
    parent_url_kwarg = "element_id"

    success_message = "Criteria created successfully ✅"

    def get_success_url(self):
        return reverse_lazy('courses:unit_detail', kwargs={
            'pk': self.object.element.unit.pk
        })
class CriteriaUpdateView(BaseChildUpdateView):
    model = PerformanceCriteria
    fields = ['description']
    template_name = "courses/criteria_form.html"

    parent_field = "element"
    parent_url_kwarg = "element_id"

    success_message = "Criteria updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:unit_detail', kwargs={
            'pk': self.object.element.unit.pk
        })
class CriteriaDeleteView(BaseChildDeleteView):
    model = PerformanceCriteria
    template_name = "courses/criteria_confirm_delete.html"

    parent_field = "element"
    parent_url_kwarg = "element_id"

    success_message = "Criteria deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:unit_detail', kwargs={
            'pk': self.object.element.unit.pk
        })




class CriteriaDetailView(BaseDetailView):
    model = PerformanceCriteria
    template_name = "courses/criteria_detail.html"
    context_object_name = "criteria"

    def get_extra_context(self):
        return {
            "element": self.object.element,
            "unit": self.object.element.unit
        }

class CriteriaUpdateView(BaseChildUpdateView):
    model = PerformanceCriteria
    fields = ['description']
    template_name = "courses/criteria_form.html"

    parent_field = "element"
    parent_url_kwarg = "element_id"

    success_message = "Criteria updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:unit_detail', kwargs={
            'pk': self.object.element.unit.pk
        })

class CriteriaDeleteView(BaseChildDeleteView):
    model = PerformanceCriteria
    template_name = "courses/criteria_delete.html"

    parent_field = "element"
    parent_url_kwarg = "element_id"

    success_message = "Criteria deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:unit_detail', kwargs={
            'pk': self.object.element.unit.pk
        })
