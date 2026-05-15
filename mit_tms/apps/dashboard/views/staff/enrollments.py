from apps.enrollment.models import (
    Enrollment
)

from ..base import (
    BaseView
)


class StaffEnrollmentsView(BaseView):

    template_name = (
        "staff/enrollments/list.html"
    )

    allowed_roles = ['STAFF']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        enrollments = (
            Enrollment.objects
            .select_related(
                'student',
                'course',
                'batch'
            )
            .all()
        )

        context.update({

            'enrollments':
                enrollments,

            'total_enrollments':
                enrollments.count(),
        })

        return context
