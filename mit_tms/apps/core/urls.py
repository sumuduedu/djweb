from django.urls import path


from .views import (
    HomeView,
    AdminDashboardView,
    StaffDashboardView,
    TeacherDashboardView,
    StudentDashboardView,
    ParentDashboardView,
    GuestDashboardView,
    dashboard_redirect,
    StudentCoursesView,
    StudentAttendanceView,
    AlumniDashboardView,
)

app_name = "core"

urlpatterns = [

    path('', HomeView.as_view(), name='home'),

    path('dashboard/', dashboard_redirect, name='dashboard'),

    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/staff/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('dashboard/teacher/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/parent/', ParentDashboardView.as_view(), name='parent_dashboard'),
    path('dashboard/guest/', GuestDashboardView.as_view(), name='guest_dashboard'),
    path('dashboard/alumni/', AlumniDashboardView.as_view(), name='alumni_dashboard'),

    path('student/courses/', StudentCoursesView.as_view(), name='student_courses'),
    path('student/attendance/', StudentAttendanceView.as_view(), name='student_attendance'),


]
