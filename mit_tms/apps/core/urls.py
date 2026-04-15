from django.urls import path
from apps.enrollment.views import apply_student, apply_teacher, apply_parent

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

    path('apply/student/<int:course_id>/', apply_student, name='apply_student'),
    path('apply/teacher/<int:course_id>/', apply_teacher, name='apply_teacher'),
    path('apply/parent/<int:course_id>/', apply_parent, name='apply_parent'),
]
