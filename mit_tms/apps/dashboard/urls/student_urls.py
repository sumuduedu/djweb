from django.urls import path


# =========================================================
# STUDENT COURSE VIEWS
# =========================================================

from apps.dashboard.views.student.courses import (
    StudentCoursesView
)


# =========================================================
# STUDENT ATTENDANCE VIEWS
# =========================================================

# from apps.dashboard.views.student.attendance import (
#     StudentAttendanceView
# )


# =========================================================
# STUDENT PAYMENT VIEWS
# =========================================================

# from apps.dashboard.views.student.payments import (
#     StudentPaymentView,
#     StudentReceiptsView,
# )


# =========================================================
# STUDENT ASSIGNMENT VIEWS
# =========================================================

# from apps.dashboard.views.student.assignments import (
#     StudentAssignmentsView
# )


# =========================================================
# STUDENT RESULT VIEWS
# =========================================================

# from apps.dashboard.views.student.results import (
#     StudentResultsView
# )


# =========================================================
# STUDENT PROGRESS VIEWS
# =========================================================

# from apps.dashboard.views.student.progress import (
#     StudentProgressView
# )


# =========================================================
# STUDENT NOTIFICATION VIEWS
# =========================================================
#
# from apps.dashboard.views.student.notifications import (
#     StudentNotificationsView
# )


# =========================================================
# STUDENT MATERIAL VIEWS
# =========================================================
#
# from apps.dashboard.views.student.materials import (
#     StudentMaterialsView
# )


# =========================================================
# STUDENT CERTIFICATE VIEWS
# =========================================================

# from apps.dashboard.views.student.certificates import (
#     StudentCertificateView
# )


# =========================================================
# STUDENT MESSAGE VIEWS
# =========================================================

# from apps.dashboard.views.student.messages import (
#     StudentMessagesView
# )


# =========================================================
# STUDENT ANNOUNCEMENT VIEWS
# =========================================================

# from apps.dashboard.views.student.announcements import (
#     StudentAnnouncementsView
# )


# =========================================================
# STUDENT ANALYTICS VIEWS
# =========================================================

# from apps.dashboard.views.student.analytics import (
#     StudentInsights,
#     StudentRiskView,
#     StudentRecommendationsView,
# )


urlpatterns = [

    # =====================================================
    # COURSES
    # =====================================================

    path(
        'courses/',
        StudentCoursesView.as_view(),
        name='student_courses'
    ),

    # =====================================================
    # ATTENDANCE
    # =====================================================

    # path(
    #     'attendance/',
    #     StudentAttendanceView.as_view(),
    #     name='student_attendance'
    # ),
    #
    # # =====================================================
    # # PAYMENTS
    # # =====================================================
    #
    # path(
    #     'payments/',
    #     StudentPaymentView.as_view(),
    #     name='student_payments'
    # ),
    #
    # path(
    #     'receipts/',
    #     StudentReceiptsView.as_view(),
    #     name='student_receipts'
    # ),
    #
    # # =====================================================
    # # ASSIGNMENTS
    # # =====================================================
    #
    # path(
    #     'assignments/',
    #     StudentAssignmentsView.as_view(),
    #     name='student_assignments'
    # ),
    #
    # # =====================================================
    # # RESULTS
    # # =====================================================
    #
    # path(
    #     'results/',
    #     StudentResultsView.as_view(),
    #     name='student_results'
    # ),
    #
    # # =====================================================
    # # PROGRESS
    # # =====================================================
    #
    # path(
    #     'progress/',
    #     StudentProgressView.as_view(),
    #     name='student_progress'
    # ),
    #
    # # =====================================================
    # # NOTIFICATIONS
    # # =====================================================
    #
    # path(
    #     'notifications/',
    #     StudentNotificationsView.as_view(),
    #     name='student_notifications'
    # ),
    #
    # # =====================================================
    # # MATERIALS
    # # =====================================================
    #
    # path(
    #     'materials/',
    #     StudentMaterialsView.as_view(),
    #     name='student_materials'
    # ),
    #
    # # =====================================================
    # # CERTIFICATES
    # # =====================================================
    #
    # path(
    #     'certificates/',
    #     StudentCertificateView.as_view(),
    #     name='student_certificates'
    # ),
    #
    # # =====================================================
    # # MESSAGES
    # # =====================================================
    #
    # path(
    #     'messages/',
    #     StudentMessagesView.as_view(),
    #     name='student_messages'
    # ),
    #
    # # =====================================================
    # # ANNOUNCEMENTS
    # # =====================================================
    #
    # path(
    #     'announcements/',
    #     StudentAnnouncementsView.as_view(),
    #     name='student_announcements'
    # ),
    #
    # # =====================================================
    # # ANALYTICS
    # # =====================================================
    #
    # path(
    #     'insights/',
    #     StudentInsights.as_view(),
    #     name='student_insights'
    # ),
    #
    # path(
    #     'risk/',
    #     StudentRiskView.as_view(),
    #     name='student_risk'
    # ),
    #
    # path(
    #     'recommendations/',
    #     StudentRecommendationsView.as_view(),
    #     name='student_recommendations'
    # ),
]
