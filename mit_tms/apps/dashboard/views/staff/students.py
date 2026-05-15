from apps.accounts.models import (
    Student
)

from ..base import (
    BaseView
)


class StaffStudentsView(BaseView):

    template_name = (
        "staff/students/list.html"
    )

    allowed_roles = ['STAFF']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        students = (
            Student.objects
            .select_related('user')
            .all()
            .order_by('full_name')
        )

        context.update({

            'students':
                students,

            'total_students':
                students.count(),
        })

        return context
