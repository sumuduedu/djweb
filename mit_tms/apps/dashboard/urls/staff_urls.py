from django.urls import path


# =========================================================
# MANAGEMENT
# =========================================================

from apps.dashboard.views.staff.students import (
    StaffStudentsView
)

from apps.dashboard.views.staff.teachers import (
    StaffTeachersView
)

from apps.dashboard.views.staff.courses import (
    StaffCoursesView
)

from apps.dashboard.views.staff.batches import (
    StaffBatchesView
)


# =========================================================
# OPERATIONS
# =========================================================

from apps.dashboard.views.staff.enrollments import (
    StaffEnrollmentsView
)

# from apps.dashboard.views.staff.attendance import (
#     StaffAttendanceView
# )
#
# from apps.dashboard.views.staff.payments import (
#     StaffPaymentsView,
#     StaffInvoicesView,
# )
#
# from apps.dashboard.views.staff.certificates import (
#     StaffCertificatesView
# )
#
# from apps.dashboard.views.staff.timetable import (
#     StaffTimetableView
# )
#
#
# # =========================================================
# # REPORTS & ANALYTICS
# # =========================================================
#
# from apps.dashboard.views.staff.reports import (
#     StaffReportsView
# )
#
# from apps.dashboard.views.staff.analytics import (
#     StaffAnalyticsView
# )
#
#
# # =========================================================
# # COMMUNICATION
# # =========================================================
#
# from apps.dashboard.views.staff.communication import (
#     StaffMessagesView,
#     StaffNotificationsView,
#     StaffAnnouncementsView,
# )
#
#
# # =========================================================
# # SETTINGS
# # =========================================================
#
# from apps.dashboard.views.staff.settings import (
#     StaffSettingsView
# )


urlpatterns = [

    # =====================================================
    # MANAGEMENT
    # =====================================================

    path(
        'students/',
        StaffStudentsView.as_view(),
        name='staff_students'
    ),

    path(
        'teachers/',
        StaffTeachersView.as_view(),
        name='staff_teachers'
    ),

    path(
        'courses/',
        StaffCoursesView.as_view(),
        name='staff_courses'
    ),

    path(
        'batches/',
        StaffBatchesView.as_view(),
        name='staff_batches'
    ),

    # =====================================================
    # OPERATIONS
    # =====================================================

    path(
        'enrollments/',
        StaffEnrollmentsView.as_view(),
        name='staff_enrollments'
    ),

    # path(
    #     'attendance/',
    #     StaffAttendanceView.as_view(),
    #     name='staff_attendance'
    # ),
    #
    # path(
    #     'payments/',
    #     StaffPaymentsView.as_view(),
    #     name='staff_payments'
    # ),
    #
    # path(
    #     'invoices/',
    #     StaffInvoicesView.as_view(),
    #     name='staff_invoices'
    # ),
    #
    # path(
    #     'certificates/',
    #     StaffCertificatesView.as_view(),
    #     name='staff_certificates'
    # ),
    #
    # path(
    #     'timetable/',
    #     StaffTimetableView.as_view(),
    #     name='staff_timetable'
    # ),
    #
    # # =====================================================
    # # REPORTS & ANALYTICS
    # # =====================================================
    #
    # path(
    #     'reports/',
    #     StaffReportsView.as_view(),
    #     name='staff_reports'
    # ),
    #
    # path(
    #     'analytics/',
    #     StaffAnalyticsView.as_view(),
    #     name='staff_analytics'
    # ),
    #
    # # =====================================================
    # # COMMUNICATION
    # # =====================================================
    #
    # path(
    #     'messages/',
    #     StaffMessagesView.as_view(),
    #     name='staff_messages'
    # ),
    #
    # path(
    #     'notifications/',
    #     StaffNotificationsView.as_view(),
    #     name='staff_notifications'
    # ),
    #
    # path(
    #     'announcements/',
    #     StaffAnnouncementsView.as_view(),
    #     name='staff_announcements'
    # ),
    #
    # # =====================================================
    # # SETTINGS
    # # =====================================================
    #
    # path(
    #     'settings/',
    #     StaffSettingsView.as_view(),
    #     name='staff_settings'
    # ),
]
