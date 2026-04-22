from django.urls import reverse_lazy

from .base import (
    BaseChildCreateView,
    BaseChildUpdateView,
    BaseChildDeleteView
)

from ..models import Assessment
from django.urls import reverse_lazy

from .base import (
    BaseChildCreateView,
    BaseChildUpdateView,
    BaseChildDeleteView,
    BaseChildListView
)

from ..models import TaskAssessment, Task
from django.shortcuts import get_object_or_404

class AssessmentCreateView(BaseChildCreateView):
    model = Assessment
    fields = ['title', 'type', 'max_marks']
    template_name = "courses/assessment_form.html"

    parent_field = "course"
    parent_url_kwarg = "course_id"

    success_message = "Assessment created successfully ✅"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })

class AssessmentUpdateView(BaseChildUpdateView):
    model = Assessment
    fields = ['title', 'type', 'max_marks']
    template_name = "courses/assessment_form.html"

    parent_field = "course"
    parent_url_kwarg = "course_id"

    success_message = "Assessment updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })
class AssessmentDeleteView(BaseChildDeleteView):
    model = Assessment
    template_name = "courses/assessment_confirm_delete.html"

    parent_field = "course"
    parent_url_kwarg = "course_id"

    success_message = "Assessment deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })


class TaskAssessmentListView(BaseChildListView):
    model = TaskAssessment
    template_name = "courses/task_assessment_list.html"
    context_object_name = "assessments"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = get_object_or_404(Task, id=self.kwargs["task_id"])
        return context

class TaskAssessmentCreateView(BaseChildCreateView):
    model = TaskAssessment
    fields = ['title', 'type', 'max_marks']
    template_name = "courses/task_assessment_form.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Task assessment created successfully ✅"

    def get_success_url(self):
        return reverse_lazy('courses:task_detail', kwargs={
            'pk': self.object.task.pk
        })
class TaskAssessmentUpdateView(BaseChildUpdateView):
    model = TaskAssessment
    fields = ['title', 'type', 'max_marks']
    template_name = "courses/task_assessment_form.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Task assessment updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:task_detail', kwargs={
            'pk': self.object.task.pk
        })
class TaskAssessmentDeleteView(BaseChildDeleteView):
    model = TaskAssessment
    template_name = "courses/task_assessment_delete.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Task assessment deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:task_detail', kwargs={
            'pk': self.object.task.pk
        })
