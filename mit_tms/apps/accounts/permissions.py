from django.core.exceptions import (
    PermissionDenied
)

from django.contrib.auth.mixins import (
    UserPassesTestMixin
)


class AdminRequiredMixin(
    UserPassesTestMixin
):

    def test_func(self):

        profile = getattr(
            self.request.user,
            'profile',
            None
        )

        return (
            profile
            and
            profile.role == 'ADMIN'
        )

    def handle_no_permission(self):

        raise PermissionDenied(
            'Permission denied.'
        )
