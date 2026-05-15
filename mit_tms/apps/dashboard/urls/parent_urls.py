from django.urls import path

from apps.dashboard.views.parent.children import (
    ParentChildrenView
)

# from apps.dashboard.views.parent.attendance import (
#     ParentAttendanceView
# )
#
# from apps.dashboard.views.parent.payments import (
#     ParentPaymentsView
# )
#
# from apps.dashboard.views.parent.progress import (
#     ParentProgressView
# )
#
# from apps.dashboard.views.parent.communication import (
#     ParentMessagesView,
#     ParentNotificationsView,
# )
#
# from apps.dashboard.views.parent.settings import (
#     ParentSettingsView
# )


urlpatterns = [

    path(
        'children/',
        ParentChildrenView.as_view(),
        name='parent_children'
    ),

    # path(
    #     'attendance/',
    #     ParentAttendanceView.as_view(),
    #     name='parent_attendance'
    # ),
    #
    # path(
    #     'payments/',
    #     ParentPaymentsView.as_view(),
    #     name='parent_payments'
    # ),
    #
    # path(
    #     'progress/',
    #     ParentProgressView.as_view(),
    #     name='parent_progress'
    # ),
    #
    # path(
    #     'messages/',
    #     ParentMessagesView.as_view(),
    #     name='parent_messages'
    # ),
    #
    # path(
    #     'notifications/',
    #     ParentNotificationsView.as_view(),
    #     name='parent_notifications'
    # ),
    #
    # path(
    #     'settings/',
    #     ParentSettingsView.as_view(),
    #     name='parent_settings'
    # ),
]
