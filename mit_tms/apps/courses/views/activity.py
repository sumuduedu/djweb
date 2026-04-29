from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .base import (
    BaseChildListView,
    BaseChildCreateView,
    BaseChildUpdateView,
    BaseChildDeleteView
)
from django.urls import reverse_lazy

from .base import (
    BaseChildCreateView,
    BaseChildUpdateView,
    BaseChildDeleteView
)

# activity.py




from ..models import Activity, Task
from apps.courses.forms import ActivityForm

from .base import BaseChildListView
from ..models import LearningResource, Course
from django.shortcuts import get_object_or_404




class ActivityListView(BaseChildListView):
    model = Activity
    template_name = "courses/activity/list.html"
    context_object_name = "activities"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = get_object_or_404(Task, id=self.kwargs.get("task_id"))
        return context


class ActivityCreateView(BaseChildCreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "courses/activity/form.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Activity created successfully ✅"

    def get_task(self):
        return get_object_or_404(Task, id=self.kwargs.get("task_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.get_task()   # 🔥 FIXED
        return context

    def form_valid(self, form):
        form.instance.task = self.get_task()  # 🔥 ensure task is set
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("courses:activity_list", kwargs={
            "task_id": self.object.task.id
        })


class ActivityUpdateView(BaseChildUpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "courses/activity/form.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Activity updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy("courses:activity_list", kwargs={
            "task_id": self.object.task.id
        })

class ActivityDeleteView(BaseChildDeleteView):
    model = Activity
    template_name = "courses/activity/delete.html"

    parent_field = "task"
    parent_url_kwarg = "task_id"

    success_message = "Activity deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy("courses:activity_list", kwargs={
            "task_id": self.object.task.id
        })

class ResourceCreateView(BaseChildCreateView):
    model = LearningResource
    fields = ['name', 'type']
    template_name = "courses/resource_form.html"

    parent_field = "course"
    parent_url_kwarg = "course_id"

    success_message = "Resource created successfully ✅"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })

class ResourceUpdateView(BaseChildUpdateView):
    model = LearningResource
    fields = ['name', 'type']
    template_name = "courses/resource_form.html"

    parent_field = "course"
    parent_url_kwarg = "course_id"

    success_message = "Resource updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })
class ResourceDeleteView(BaseChildDeleteView):
    model = LearningResource
    template_name = "courses/resource_confirm_delete.html"

    parent_field = "course"
    parent_url_kwarg = "course_id"

    success_message = "Resource deleted successfully ❌"

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={
            'pk': self.object.course.pk
        })

class ResourceListView(BaseChildListView):
    model = LearningResource
    template_name = "courses/resource_list.html"
    context_object_name = "resources"

    parent_field = "course"
    parent_url_kwarg = "course_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, id=self.kwargs["course_id"])
        return context
