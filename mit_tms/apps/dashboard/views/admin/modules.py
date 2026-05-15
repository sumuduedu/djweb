from django.shortcuts import (
    get_object_or_404
)

from django.urls import (
    reverse_lazy
)

from apps.courses.models import (
    Course,
    Module
)

from ..base import (
    BaseView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView
)


# =====================================================
# MODULE LIST
# =====================================================

class AdminModuleListView(BaseView):

    template_name = (
        "admin/modules/list.html"
    )

    allowed_roles = ['ADMIN']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        modules = (
            Module.objects
            .select_related('course')
            .all()
            .order_by('-created_at')
        )

        context['modules'] = modules

        context['total_modules'] = (
            modules.count()
        )

        return context


# =====================================================
# MODULE DETAIL
# =====================================================

class AdminModuleDetailView(
    BaseDetailView
):

    model = Module

    template_name = (
        "admin/modules/detail.html"
    )

    allowed_roles = ['ADMIN']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        module = self.object

        context['tasks'] = (
            module.tasks.all()
        )

        return context


# =====================================================
# MODULE CREATE
# =====================================================

class AdminModuleCreateView(
    BaseCreateView
):

    model = Module

    template_name = (
        "admin/modules/form.html"
    )

    fields = [
        'course',
        'title',
        'code',
        'description',
        'theory_hours',
        'practical_hours',
        'order',
        'status',
    ]

    success_url = reverse_lazy(
        'dashboard:admin_modules'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Module created successfully 🎉"
    )

    def get_initial(self):

        initial = super().get_initial()

        course_id = (
            self.request.GET.get(
                'course'
            )
        )

        if course_id:

            course = get_object_or_404(
                Course,
                id=course_id
            )

            initial['course'] = course

        return initial


# =====================================================
# MODULE UPDATE
# =====================================================

class AdminModuleUpdateView(
    BaseUpdateView
):

    model = Module

    template_name = (
        "admin/modules/form.html"
    )

    fields = [
        'course',
        'title',
        'code',
        'description',
        'theory_hours',
        'practical_hours',
        'order',
        'status',
    ]

    success_url = reverse_lazy(
        'dashboard:admin_modules'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Module updated successfully ✏️"
    )


# =====================================================
# MODULE DELETE
# =====================================================

class AdminModuleDeleteView(
    BaseDeleteView
):

    model = Module

    template_name = (
        "admin/modules/delete.html"
    )

    success_url = reverse_lazy(
        'dashboard:admin_modules'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Module deleted successfully 🗑"
    )
