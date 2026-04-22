from django.urls import reverse_lazy

from .base import (
    BaseChildCreateView,
    BaseChildListView,
    BaseUpdateView,
    BaseDeleteView,
    BaseDetailView
)

from ..models import Task
from ..forms import TaskForm

from .base import (
    BaseChildCreateView,
    BaseChildUpdateView,
    BaseChildDeleteView,
    BaseChildListView
)
from django.urls import reverse_lazy
from ..models import TaskStandard, Task
from django.shortcuts import get_object_or_404

class TaskListView(BaseChildListView):
    model = Task
    template_name = "courses/task_list.html"
    context_object_name = "tasks"

    parent_field = "module"
    parent_url_kwarg = "module_id"

class TaskCreateView(BaseChildCreateView):
    model = Task
    form_class = TaskForm
    template_name = "courses/task_form.html"

    parent_field = "module"
    parent_url_kwarg = "module_id"

    success_message = "Task created successfully ✅"

    def get_success_url(self):
        return reverse_lazy('courses:module_detail', kwargs={
            'pk': self.object.module.pk
        })
class TaskUpdateView(BaseUpdateView):
    model = Task
    form_class = TaskForm
    template_name = "courses/task_form.html"

    success_message = "Task updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:module_detail', kwargs={
            'pk': self.object.module.pk
        })
class TaskDeleteView(BaseDeleteView):
    model = Task
    template_name = "courses/task_confirm_delete.html"

    success_message = "Task deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:module_detail', kwargs={
            'pk': self.object.module.pk
        })

class TaskDetailView(BaseDetailView):
    model = Task
    template_name = "courses/task_detail.html"
    context_object_name = "task"

class TaskStandardListView(BaseChildListView):
    model = TaskStandard
    template_name = "courses/task_standard_list.html"
    context_object_name = "standards"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = get_object_or_404(Task, id=self.kwargs["task_id"])
        return context
class TaskStandardCreateView(BaseChildCreateView):
    model = TaskStandard
    fields = ['description']
    template_name = "courses/task_standard_form.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Task standard created successfully ✅"

    def get_success_url(self):
        return reverse_lazy('courses:task_detail', kwargs={
            'pk': self.object.task.pk
        })
class TaskStandardUpdateView(BaseChildUpdateView):
    model = TaskStandard
    fields = ['description']
    template_name = "courses/task_standard_form.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Task standard updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:task_detail', kwargs={
            'pk': self.object.task.pk
        })
class TaskStandardDeleteView(BaseChildDeleteView):
    model = TaskStandard
    template_name = "courses/task_standard_delete.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Task standard deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:task_detail', kwargs={
            'pk': self.object.task.pk
        })
