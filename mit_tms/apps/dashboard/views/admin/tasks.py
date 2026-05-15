from django.shortcuts import (
    get_object_or_404
)

from django.urls import (
    reverse_lazy
)

from apps.courses.models import (
    Module,
    Task
)

from ..base import (
    BaseView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView
)


# =====================================================
# TASK LIST
# =====================================================

class AdminTaskListView(BaseView):

    template_name = (
        "admin/tasks/list.html"
    )

    allowed_roles = ['ADMIN']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        tasks = (
            Task.objects
            .select_related(
                'module',
                'module__course'
            )
            .all()
            .order_by('-created_at')
        )

        context['tasks'] = tasks

        context['total_tasks'] = (
            tasks.count()
        )

        return context


# =====================================================
# TASK DETAIL
# =====================================================

class AdminTaskDetailView(
    BaseDetailView
):

    model = Task

    template_name = (
        "admin/tasks/detail.html"
    )

    allowed_roles = ['ADMIN']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        task = self.object

        context['activities'] = (
            task.activities.all()
        )

        return context


# =====================================================
# TASK CREATE
# =====================================================

class AdminTaskCreateView(
    BaseCreateView
):

    model = Task

    template_name = (
        "admin/tasks/form.html"
    )

    fields = [
        'module',
        'title',
        'description',
        'order',
        'status',
    ]

    success_url = reverse_lazy(
        'dashboard:admin_tasks'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Task created successfully 🎉"
    )

    def get_initial(self):

        initial = super().get_initial()

        module_id = (
            self.request.GET.get(
                'module'
            )
        )

        if module_id:

            module = get_object_or_404(
                Module,
                id=module_id
            )

            initial['module'] = module

        return initial


# =====================================================
# TASK UPDATE
# =====================================================

class AdminTaskUpdateView(
    BaseUpdateView
):

    model = Task

    template_name = (
        "admin/tasks/form.html"
    )

    fields = [
        'module',
        'title',
        'description',
        'order',
        'status',
    ]

    success_url = reverse_lazy(
        'dashboard:admin_tasks'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Task updated successfully ✏️"
    )


# =====================================================
# TASK DELETE
# =====================================================

class AdminTaskDeleteView(
    BaseDeleteView
):

    model = Task

    template_name = (
        "admin/tasks/delete.html"
    )

    success_url = reverse_lazy(
        'dashboard:admin_tasks'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Task deleted successfully 🗑"
    )
