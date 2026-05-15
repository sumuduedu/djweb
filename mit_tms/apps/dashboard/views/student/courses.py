from django.shortcuts import (
    get_object_or_404
)

from apps.courses.models import (
    Course
)

from apps.enrollment.models import (
    Enrollment
)

from ..base import (
    BaseView,
    BaseDetailView
)


# =========================================================
# STUDENT COURSE LIST
# =========================================================

class StudentCoursesView(BaseView):

    template_name = (
        "student/courses/list.html"
    )

    allowed_roles = ['STUDENT']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        student = (
            self.request.user.student
        )

        enrollments = (
            Enrollment.objects
            .select_related(
                'course',
                'batch'
            )
            .filter(
                student=student
            )
        )

        context['enrollments'] = (
            enrollments
        )

        context['courses'] = [
            enrollment.course
            for enrollment in enrollments
        ]

        context['total_courses'] = (
            enrollments.count()
        )

        return context


# =========================================================
# STUDENT COURSE DETAIL
# =========================================================

class StudentCourseDetailView(
    BaseDetailView
):

    model = Course

    template_name = (
        "student/courses/detail.html"
    )

    allowed_roles = ['STUDENT']

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        course = self.get_object()

        student = (
            request.user.student
        )

        is_enrolled = (
            Enrollment.objects.filter(
                student=student,
                course=course
            ).exists()
        )

        if not is_enrolled:

            return self.handle_no_permission()

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        course = self.object

        context['modules'] = (
            course.modules.all()
        )

        context['resources'] = (
            course.resources.all()
        )

        return context
