from ..base import (
    BaseView
)


class AlumniCoursesView(BaseView):

    template_name = (
        "alumni/courses/index.html"
    )

    allowed_roles = ['ALUMNI']
