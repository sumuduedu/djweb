from django.urls import path
from .views import (
    HomeView,
    AdminDashboardView,
    TeacherDashboardView,
    StudentDashboardView,
    dashboard_redirect,
    StudentCoursesView,
    StudentAttendanceView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # 🔀 redirect based on role
    path('dashboard/', dashboard_redirect, name='dashboard'),

    # 🎯 role dashboards
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/teacher/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/courses/', StudentCoursesView.as_view(), name='student_courses'),
    path('student/attendance/',StudentAttendanceView.as_view(), name='student_attendance')
]
