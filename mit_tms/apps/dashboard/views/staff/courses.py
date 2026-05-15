from apps.courses.models import (
    Course
)

from ..base import (
    BaseView
)


class StaffCoursesView(BaseView):

    template_name = (
        "staff/courses/list.html"
    )

    allowed_roles = ['STAFF']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        courses = (
            Course.objects
            .all()
            .order_by('title')
        )

        context.update({

            'courses':
                courses,

            'total_courses':
                courses.count(),
        })

        return context
