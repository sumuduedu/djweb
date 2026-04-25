from django.urls import reverse_lazy

from .base import (
    BaseChildCreateView,
    BaseUpdateView,
    BaseDeleteView,
    BaseDetailView
)

from ..models import Module
from apps.courses.forms.module import ModuleForm


class ModuleCreateView(BaseChildCreateView):
    model = Module
    form_class = ModuleForm
    template_name = "courses/module_form.html"

    parent_field = "course"
    parent_url_kwarg = "course_id"

    success_message = "Module created successfully ✅"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })

class ModuleUpdateView(BaseUpdateView):
    model = Module
    form_class = ModuleForm
    template_name = "courses/module_form.html"

    success_message = "Module updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })

class ModuleDetailView(BaseDetailView):
    model = Module
    template_name = "courses/module_detail.html"
    context_object_name = "module"


class ModuleDeleteView(BaseDeleteView):
    model = Module
    template_name = "courses/module_confirm_delete.html"

    success_message = "Module deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })

