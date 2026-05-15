from django.shortcuts import (
    get_object_or_404
)

from django.urls import (
    reverse_lazy
)

from apps.courses.models import (
    Task,
    Activity
)

from ..base import (
    BaseView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView
)


# =====================================================
# ACTIVITY LIST
# =====================================================

class AdminActivityListView(BaseView):

    template_name = (
        "admin/activities/list.html"
    )

    allowed_roles = ['ADMIN']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        activities = (
            Activity.objects
            .select_related(
                'task',
                'task__module',
                'task__module__course'
            )
            .all()
            .order_by('-created_at')
        )

        context['activities'] = activities

        context['total_activities'] = (
            activities.count()
        )

        return context


# =====================================================
# ACTIVITY DETAIL
# =====================================================

class AdminActivityDetailView(
    BaseDetailView
):

    model = Activity

    template_name = (
        "admin/activities/detail.html"
    )

    allowed_roles = ['ADMIN']


# =====================================================
# ACTIVITY CREATE
# =====================================================

class AdminActivityCreateView(
    BaseCreateView
):

    model = Activity

    template_name = (
        "admin/activities/form.html"
    )

    fields = [
        'task',
        'title',
        'description',
        'duration_minutes',
        'activity_type',
        'order',
        'status',
    ]

    success_url = reverse_lazy(
        'dashboard:admin_activities'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Activity created successfully 🎉"
    )

    def get_initial(self):

        initial = super().get_initial()

        task_id = (
            self.request.GET.get(
                'task'
            )
        )

        if task_id:

            task = get_object_or_404(
                Task,
                id=task_id
            )

            initial['task'] = task

        return initial


# =====================================================
# ACTIVITY UPDATE
# =====================================================

class AdminActivityUpdateView(
    BaseUpdateView
):

    model = Activity

    template_name = (
        "admin/activities/form.html"
    )

    fields = [
        'task',
        'title',
        'description',
        'duration_minutes',
        'activity_type',
        'order',
        'status',
    ]

    success_url = reverse_lazy(
        'dashboard:admin_activities'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Activity updated successfully ✏️"
    )


# =====================================================
# ACTIVITY DELETE
# =====================================================

class AdminActivityDeleteView(
    BaseDeleteView
):

    model = Activity

    template_name = (
        "admin/activities/delete.html"
    )

    success_url = reverse_lazy(
        'dashboard:admin_activities'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Activity deleted successfully 🗑"
    )
