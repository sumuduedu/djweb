from apps.batch.models import (
    Batch
)

from ..base import (
    BaseView
)


class StaffBatchesView(BaseView):

    template_name = (
        "staff/batches/list.html"
    )

    allowed_roles = ['STAFF']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        batches = (
            Batch.objects
            .select_related(
                'course',
                'teacher'
            )
            .all()
        )

        context.update({

            'batches':
                batches,

            'total_batches':
                batches.count(),
        })

        return context
