from django.urls import path
from django.urls import path
from apps.core.views.crud import *
from .views import (
    # Home
    HomeView,
    dashboard_redirect,

    # Dashboards
    AdminDashboardView,
    StaffDashboardView,
    TeacherDashboardView,
    StudentDashboardView,
    ParentDashboardView,
    GuestDashboardView,
    AlumniDashboardView,

    # Admin Views
    AdminCourseView,


    # Student Views
    StudentCoursesView,
    StudentAttendanceView,
    StudentPaymentView,

    # (Add these views later as you create them)
    StudentAssignmentsView,
    StudentResultsView,
    StudentProgressView,
    StudentNotificationsView,
    StudentMaterialsView,
    StudentCertificateView,
    StudentMessagesView,
    StudentAnnouncementsView,
    StudentReceiptsView,
    StudentInsights,
    StudentRiskView,
    StudentRecommendationsView,


    # Teacher Views
    TeacherCoursesView,
    TeacherAssignmentsView,
    TeacherStudentsView,
    TeacherAttendanceView,
    TeacherResultsView,
    TeacherMaterialsView,
    TeacherSubmissionsView,
    TeacherPerformanceView,
    TeacherRiskStudentsView,
    TeacherAnalyticsView,
    TeacherNotificationsView,
    TeacherMessagesView,
    TeacherAnnouncementsView,

    #StaffViews,
    StaffStudentsView,
    StaffPaymentsView,
    StaffEnrollmentsView,
    StaffReportsView,
    StaffBatchesView,
    StaffAttendanceView,
    StaffInvoicesView,
    StaffNotificationsView,

    # Parent Views
    ParentChildrenView,
    ParentProgressView,
    ParentAttendanceView,
    ParentPaymentsView,
    ParentResultsView,
    ParentMessagesView,
    ParentNotificationsView,

    # Alumni Views
     AlumniJobsView,
     AlumniEventsView,
     AlumniEventsView,
     AlumniNetworkView,
     AlumniCertificatesView,
)

app_name = "core"

urlpatterns = [

    # ================= HOME =================
    path('', HomeView.as_view(), name='home'),

    # ================= REDIRECT =================
    path('dashboard/', dashboard_redirect, name='dashboard'),


    # ================= DASHBOARDS =================
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/staff/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('dashboard/teacher/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/parent/', ParentDashboardView.as_view(), name='parent_dashboard'),
    path('dashboard/guest/', GuestDashboardView.as_view(), name='guest_dashboard'),
    path('dashboard/alumni/', AlumniDashboardView.as_view(), name='alumni_dashboard'),


    # ==================Admin Dashboards =====================
    path('dashboard/courses/', AdminCourseView.as_view(), name='admin_courses'),



    # =====================================================
    # 🎓 STUDENT MODULE
    # =====================================================
    path('student/courses/', StudentCoursesView.as_view(), name='student_courses'),
    path('student/attendance/', StudentAttendanceView.as_view(), name='student_attendance'),
    path('student/payment/', StudentPaymentView.as_view(), name='student_payment'),

    # Future (recommended)
    path('student/assignments/', StudentAssignmentsView.as_view(), name='student_assignments'),
    path('student/results/', StudentResultsView.as_view(), name='student_results'),
    path('student/progress/', StudentProgressView.as_view(), name='student_progress'),
    path('student/notifications/', StudentNotificationsView.as_view(), name='student_notifications'),
    path('student/materials/', StudentMaterialsView.as_view(), name='student_materials'),
    path('student/certificates/', StudentCertificateView.as_view(), name='student_certificates'),
    path('student/messages/', StudentMessagesView.as_view(), name='student_messages'),
    path('student/announcements/', StudentAnnouncementsView.as_view(), name='student_announcements'),
    path('student/receipts/', StudentReceiptsView.as_view(), name='student_receipts'),
    path('student/insights/', StudentInsights.as_view(), name='student_insights'),
    path('student/risk/', StudentRiskView.as_view(), name='student_risk'),
    path('student/recommendations/', StudentRecommendationsView.as_view(), name='student_recommendations'),


    # =====================================================
    # 👨‍🏫 TEACHER MODULE
    # =====================================================
    path('teacher/courses/', TeacherCoursesView.as_view(), name='teacher_courses'),
    path('teacher/assignments/', TeacherAssignmentsView.as_view(), name='teacher_assignments'),
    path('teacher/students/', TeacherStudentsView.as_view(), name='teacher_students'),
    path('teacher/attendance/', TeacherAttendanceView.as_view(), name='teacher_attendance'),
    path('teacher/results/', TeacherResultsView.as_view(), name='teacher_results'),
    path('teacher/materials/', TeacherMaterialsView.as_view(), name='teacher_materials'),
    path('teacher/submissions/', TeacherSubmissionsView.as_view(), name='teacher_submissions'),
    path('teacher/performance/', TeacherPerformanceView.as_view(), name='teacher_performance'),
    path('teacher/risk-students/', TeacherRiskStudentsView.as_view(), name='teacher_risk_students'),
    path('teacher/analytics/', TeacherAnalyticsView.as_view(), name='teacher_analytics'),
    path('teacher/notifications/', TeacherNotificationsView.as_view(), name='teacher_notifications'),
    path('teacher/messages/', TeacherMessagesView.as_view(), name='teacher_messages'),
    path('teacher/announcements/', TeacherAnnouncementsView.as_view(), name='teacher_announcements'),


    # =====================================================
    # 🧑‍💼 STAFF MODULE
    # =====================================================
    path('staff/students/', StaffStudentsView.as_view(), name='staff_students'),
    path('staff/enrollments/', StaffEnrollmentsView.as_view(), name='staff_enrollments'),
    path('staff/payments/', StaffPaymentsView.as_view(), name='staff_payments'),
    path('staff/reports/', StaffReportsView.as_view(), name='staff_reports'),
    path('staff/batches/', StaffBatchesView.as_view(), name='staff_batches'),
    path('staff/attendance/', StaffAttendanceView.as_view(), name='staff_attendance'),
    path('staff/invoices/', StaffInvoicesView.as_view(), name='staff_invoices'),
    path('staff/notifications/', StaffNotificationsView.as_view(), name='staff_notifications'),
    # =====================================================
    # 👨‍👩‍👧 PARENT MODULE
    # =====================================================
    path('parent/children/', ParentChildrenView.as_view(), name='parent_children'),
    path('parent/progress/', ParentProgressView.as_view(), name='parent_progress'),
    path('parent/attendance/', ParentAttendanceView.as_view(), name='parent_attendance'),
    path('parent/payments/', ParentPaymentsView.as_view(), name='parent_payments'),
    path('parent/results/', ParentResultsView.as_view(), name='parent_results'),
    path('parent/messages/', ParentMessagesView.as_view(), name='parent_messages'),
    path('parent/notifications/', ParentNotificationsView.as_view(), name='parent_notifications'),
    # =====================================================
    # 🎓 ALUMNI MODULE
    # =====================================================
     path('alumni/jobs/', AlumniJobsView.as_view(), name='alumni_jobs'),
     path('alumni/events/', AlumniEventsView.as_view(), name='alumni_events'),
     path('alumni/network/', AlumniNetworkView.as_view(), name='alumni_network'),
     path('alumni/certificates/', AlumniCertificatesView.as_view(), name='alumni_certificates'),
    #=====================================================
    #🔥 DYNAMIC CRUD SYSTEM (SAFE ZONE)
    #=====================================================
    path('manage/<str:entity>/', DynamicListView.as_view(), name='dynamic_list'),
    path('manage/<str:entity>/add/', DynamicCreateView.as_view(), name='dynamic_create'),
    path('manage/<str:entity>/<int:pk>/edit/', DynamicUpdateView.as_view(), name='dynamic_update'),
    path('manage/<str:entity>/<int:pk>/delete/', DynamicDeleteView.as_view(), name='dynamic_delete'),

]




