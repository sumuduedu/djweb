from django.shortcuts import (
    get_object_or_404
)

from apps.courses.models import (
    Course
)

from apps.batch.models import (
    Batch
)

from apps.enrollment.models import (
    Enrollment
)

from ..base import (
    BaseView,
    BaseDetailView
)


# =========================================================
# TEACHER COURSES VIEW
# =========================================================

class TeacherCoursesView(BaseView):

    template_name = (
        "teacher/courses/list.html"
    )

    allowed_roles = ['TEACHER']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        teacher = (
            self.request.user.teacher
        )

        # =================================================
        # BATCHES ASSIGNED TO TEACHER
        # =================================================

        batches = (
            Batch.objects
            .select_related(
                'course'
            )
            .filter(
                teacher=teacher
            )
        )

        # =================================================
        # COURSES
        # =================================================

        courses = (
            Course.objects.filter(
                batches__teacher=teacher
            )
            .distinct()
        )

        # =================================================
        # TOTAL STUDENTS
        # =================================================

        total_students = (
            Enrollment.objects.filter(
                batch__teacher=teacher
            ).count()
        )

        context.update({

            'batches':
                batches,

            'courses':
                courses,

            'total_courses':
                courses.count(),

            'total_batches':
                batches.count(),

            'total_students':
                total_students,
        })

        return context


# =========================================================
# TEACHER COURSE DETAIL
# =========================================================

class TeacherCourseDetailView(
    BaseDetailView
):

    model = Course

    template_name = (
        "teacher/courses/detail.html"
    )

    allowed_roles = ['TEACHER']

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        course = self.get_object()

        teacher = (
            request.user.teacher
        )

        has_access = (
            Batch.objects.filter(
                teacher=teacher,
                course=course
            ).exists()
        )

        if not has_access:

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

        teacher = (
            self.request.user.teacher
        )

        batches = (
            Batch.objects.filter(
                teacher=teacher,
                course=course
            )
        )

        modules = (
            course.modules.all()
        )

        enrollments = (
            Enrollment.objects.filter(
                batch__in=batches
            )
            .select_related(
                'student'
            )
        )

        context.update({

            'batches':
                batches,

            'modules':
                modules,

            'enrollments':
                enrollments,

            'total_students':
                enrollments.count(),
        })

        return context
