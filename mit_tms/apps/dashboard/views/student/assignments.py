
from django.utils.timezone import (
    now
)

from apps.assessment.models import (
    Assignment,
    AssignmentSubmission
)

from ..base import (
    BaseView
)


# =========================================================
# STUDENT ASSIGNMENTS VIEW
# =========================================================

class StudentAssignmentsView(BaseView):

    template_name = (
        "student/assignments/list.html"
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

        # =================================================
        # STUDENT SUBMISSIONS
        # =================================================

        submissions = (
            AssignmentSubmission.objects
            .select_related(
                'assignment',
                'assignment__module',
                'assignment__course'
            )
            .filter(
                student=student
            )
        )

        # =================================================
        # ASSIGNMENTS
        # =================================================

        assignments = (
            Assignment.objects
            .select_related(
                'module',
                'course'
            )
            .all()
            .order_by(
                'due_date'
            )
        )

        # =================================================
        # COUNTS
        # =================================================

        total_assignments = (
            assignments.count()
        )

        submitted_count = (
            submissions.count()
        )

        pending_count = (
            total_assignments -
            submitted_count
        )

        overdue_count = (
            assignments.filter(
                due_date__lt=now(),
                is_active=True
            ).count()
        )

        # =================================================
        # CONTEXT
        # =================================================

        context.update({

            'assignments':
                assignments,

            'submissions':
                submissions,

            'total_assignments':
                total_assignments,

            'submitted_count':
                submitted_count,

            'pending_count':
                pending_count,

            'overdue_count':
                overdue_count,
        })

        return context
