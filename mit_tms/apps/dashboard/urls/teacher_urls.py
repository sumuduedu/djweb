from django.urls import path

from django.urls import path


# =========================================================
# TEACHER COURSE VIEWS
# =========================================================

from apps.dashboard.views.teacher.courses import (
    TeacherCoursesView,
    TeacherCourseDetailView,
)

urlpatterns = [

    path(
        'courses/',
        TeacherCoursesView.as_view(),
        name='teacher_courses'
    ),

    path(
        'courses/<int:pk>/',
        TeacherCourseDetailView.as_view(),
        name='teacher_course_detail'
    ),
    #
    # path(
    #     'assignments/',
    #     TeacherAssignmentsView.as_view(),
    #     name='teacher_assignments'
    # ),
    #
    # path(
    #     'students/',
    #     TeacherStudentsView.as_view(),
    #     name='teacher_students'
    # ),
    #
    # path(
    #     'attendance/',
    #     TeacherAttendanceView.as_view(),
    #     name='teacher_attendance'
    # ),
    #
    # path(
    #     'results/',
    #     TeacherResultsView.as_view(),
    #     name='teacher_results'
    # ),
    #
    # path(
    #     'materials/',
    #     TeacherMaterialsView.as_view(),
    #     name='teacher_materials'
    # ),
    #
    # path(
    #     'submissions/',
    #     TeacherSubmissionsView.as_view(),
    #     name='teacher_submissions'
    # ),
    #
    # path(
    #     'performance/',
    #     TeacherPerformanceView.as_view(),
    #     name='teacher_performance'
    # ),
    #
    # path(
    #     'risk-students/',
    #     TeacherRiskStudentsView.as_view(),
    #     name='teacher_risk_students'
    # ),
    #
    # path(
    #     'analytics/',
    #     TeacherAnalyticsView.as_view(),
    #     name='teacher_analytics'
    # ),
    #
    # path(
    #     'notifications/',
    #     TeacherNotificationsView.as_view(),
    #     name='teacher_notifications'
    # ),
    #
    # path(
    #     'messages/',
    #     TeacherMessagesView.as_view(),
    #     name='teacher_messages'
    # ),
    #
    # path(
    #     'announcements/',
    #     TeacherAnnouncementsView.as_view(),
    #     name='teacher_announcements'
    # ),
]
