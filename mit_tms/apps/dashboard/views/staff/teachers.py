from apps.accounts.models import (
    Teacher
)

from ..base import (
    BaseView
)


class StaffTeachersView(BaseView):

    template_name = (
        "staff/teachers/list.html"
    )

    allowed_roles = ['STAFF']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        teachers = (
            Teacher.objects
            .select_related('user')
            .all()
            .order_by('full_name')
        )

        context.update({

            'teachers':
                teachers,

            'total_teachers':
                teachers.count(),
        })

        return context
