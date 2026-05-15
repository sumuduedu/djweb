from django.db.models import Sum

from django.forms import (
    inlineformset_factory
)

from django.shortcuts import (
    get_object_or_404
)

from django.urls import (
    reverse_lazy
)

from apps.courses.models import (
    Course,
    NCS
)

from apps.courses.models.resource import (
    LearningResource
)

from apps.enrollment.models import (
    Enrollment
)

from ..base import (
    BaseView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView
)


# =====================================================
# RESOURCE FORMSET
# =====================================================

LearningResourceFormSet = (
    inlineformset_factory(
        Course,
        LearningResource,
        fields=[
            'name',
            'type',
            'file',
            'url',
            'description'
        ],
        extra=1,
        can_delete=True
    )
)


# =====================================================
# COURSE LIST
# =====================================================

class AdminCourseListView(BaseView):

    template_name = (
        "admin/courses/list.html"
    )

    allowed_roles = ['ADMIN']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        courses = (
            Course.objects.all()
            .order_by('-created_at')
        )

        context['courses'] = courses

        context['total_courses'] = (
            courses.count()
        )

        context['active_courses'] = (
            Course.objects.filter(
                status='ACTIVE'
            ).count()
        )

        context['total_students_enrolled'] = (
            Enrollment.objects.count()
        )

        context['current_ncs_version'] = (
            NCS.objects.filter(
                is_active=True
            ).first()
        )

        return context


# =====================================================
# COURSE DETAIL
# =====================================================

class AdminCourseDetailView(
    BaseDetailView
):

    model = Course

    template_name = (
        "admin/courses/detail.html"
    )

    allowed_roles = ['ADMIN']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        course = self.object

        modules = (
            course.modules.all()
        )

        total_theory = (
            modules.aggregate(
                total=Sum(
                    'theory_hours'
                )
            )['total'] or 0
        )

        total_practical = (
            modules.aggregate(
                total=Sum(
                    'practical_hours'
                )
            )['total'] or 0
        )

        context.update({

            'modules': modules,

            'total_theory':
                total_theory,

            'total_practical':
                total_practical,

            'total_hours_sum':
                (
                    total_theory +
                    total_practical
                ),

            'is_matching':
                (
                    total_theory ==
                    (
                        course.theory_hours
                        or 0
                    )
                    and
                    total_practical ==
                    (
                        course.practical_hours
                        or 0
                    )
                )
        })

        return context


# =====================================================
# COURSE CREATE
# =====================================================

class AdminCourseCreateView(
    BaseCreateView
):

    model = Course

    template_name = (
        "admin/courses/form.html"
    )

    fields = [
        'title',
        'code',
        'description',
        'status',
        'theory_hours',
        'practical_hours',
        'assignment_hours',
        'duration_months',
        'course_fee',
        'is_free',
    ]

    success_url = reverse_lazy(
        'dashboard:admin_courses'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Course created successfully 🎉"
    )

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        if self.request.POST:

            context[
                'resource_formset'
            ] = LearningResourceFormSet(
                self.request.POST,
                self.request.FILES
            )

        else:

            context[
                'resource_formset'
            ] = LearningResourceFormSet()

        return context

    def form_valid(
        self,
        form
    ):

        context = self.get_context_data()

        formset = (
            context[
                'resource_formset'
            ]
        )

        if formset.is_valid():

            self.object = form.save()

            formset.instance = self.object

            formset.save()

            return super().form_valid(
                form
            )

        return self.form_invalid(
            form
        )


# =====================================================
# COURSE UPDATE
# =====================================================

class AdminCourseUpdateView(
    BaseUpdateView
):

    model = Course

    template_name = (
        "admin/courses/form.html"
    )

    fields = [
        'title',
        'code',
        'description',
        'status',
        'theory_hours',
        'practical_hours',
        'assignment_hours',
        'duration_months',
        'course_fee',
        'is_free',
    ]

    success_url = reverse_lazy(
        'dashboard:admin_courses'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Course updated successfully ✏️"
    )


# =====================================================
# COURSE DELETE
# =====================================================

class AdminCourseDeleteView(
    BaseDeleteView
):

    model = Course

    template_name = (
        "admin/courses/delete.html"
    )

    success_url = reverse_lazy(
        'dashboard:admin_courses'
    )

    allowed_roles = ['ADMIN']

    success_message = (
        "Course deleted successfully 🗑"
    )
