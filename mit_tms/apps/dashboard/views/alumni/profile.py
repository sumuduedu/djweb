from ..base import (
    BaseView
)


class AlumniProfileView(BaseView):

    template_name = (
        "alumni/profile/index.html"
    )

    allowed_roles = ['ALUMNI']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        context['alumni'] = (
            self.request.user.alumni
        )

        return context
