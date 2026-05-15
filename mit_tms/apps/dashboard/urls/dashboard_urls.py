from django.urls import path

from apps.dashboard.views import (
    HomeView,
    dashboard_redirect
)

from apps.dashboard.views.dashboards.admin import (
    AdminDashboardView
)

from apps.dashboard.views.dashboards.student import (
    StudentDashboardView
)

from apps.dashboard.views.dashboards.teacher import (
    TeacherDashboardView
)

from apps.dashboard.views.dashboards.staff import (
    StaffDashboardView
)

from apps.dashboard.views.dashboards.parent import (
    ParentDashboardView
)

from apps.dashboard.views.dashboards.alumni import (
    AlumniDashboardView
)

from apps.dashboard.views.dashboards.guest import (
    GuestDashboardView
)


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        '',
        HomeView.as_view(),
        name='home'
    ),

    # =====================================================
    # DASHBOARD REDIRECT
    # =====================================================

    path(
        'dashboard/',
        dashboard_redirect,
        name='dashboard_redirect'
    ),

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        'dashboard/admin/',
        AdminDashboardView.as_view(),
        name='admin_dashboard'
    ),

    # =====================================================
    # STUDENT
    # =====================================================

    path(
        'dashboard/student/',
        StudentDashboardView.as_view(),
        name='student_dashboard'
    ),

    # =====================================================
    # TEACHER
    # =====================================================

    path(
        'dashboard/teacher/',
        TeacherDashboardView.as_view(),
        name='teacher_dashboard'
    ),

    # =====================================================
    # STAFF
    # =====================================================

    path(
        'dashboard/staff/',
        StaffDashboardView.as_view(),
        name='staff_dashboard'
    ),

    # =====================================================
    # PARENT
    # =====================================================

    path(
        'dashboard/parent/',
        ParentDashboardView.as_view(),
        name='parent_dashboard'
    ),

    # =====================================================
    # ALUMNI
    # =====================================================

    path(
        'dashboard/alumni/',
        AlumniDashboardView.as_view(),
        name='alumni_dashboard'
    ),

    # =====================================================
    # GUEST
    # =====================================================

    path(
        'dashboard/guest/',
        GuestDashboardView.as_view(),
        name='guest_dashboard'
    ),
]
