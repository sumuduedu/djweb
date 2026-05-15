from apps.accounts.models import (
    Parent
)

from ..base import (
    BaseView
)


class ParentChildrenView(BaseView):

    template_name = (
        "parent/children/list.html"
    )

    allowed_roles = ['PARENT']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        parent = (
            self.request.user.parent
        )

        students = (
            parent.students.all()
        )

        context.update({

            'students':
                students,

            'total_students':
                students.count(),
        })

        return context
