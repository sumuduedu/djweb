from django.urls import reverse_lazy
from django.shortcuts import redirect

from .base import BaseUpdateView, BaseDeleteView, BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from ..models import Unit, Course
from ..forms import UnitForm, ElementFormSet
from django.contrib import messages

class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = "courses/unit_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['elements'] = ElementFormSet(self.request.POST)
        else:
            data['elements'] = ElementFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        elements = context['elements']

        # 🔥 attach course
        form.instance.course_id = self.kwargs['course_id']

        if elements.is_valid():
            self.object = form.save()

            elements.instance = self.object
            elements.save()

            messages.success(self.request, "Unit + Elements created successfully ✅")
            return redirect(self.get_success_url())

        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })

class UnitUpdateView(BaseUpdateView):
    model = Unit
    form_class = UnitForm
    template_name = "courses/unit_form.html"

    success_message = "Unit updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })

class UnitDeleteView(BaseDeleteView):
    model = Unit
    template_name = "courses/unit_confirm_delete.html"

    success_message = "Unit deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })
class UnitDetailView(BaseDetailView):
    model = Unit
    template_name = "courses/unit_detail.html"
    context_object_name = "unit"

class CourseNCSView(BaseDetailView):
    model = Course
    template_name = "courses/course_ncs.html"
    context_object_name = "course"

