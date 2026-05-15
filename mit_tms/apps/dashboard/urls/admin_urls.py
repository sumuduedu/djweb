from django.urls import path


# =========================================================
# COURSE VIEWS
# =========================================================

from apps.dashboard.views.admin.courses import (

    AdminCourseListView,
    AdminCourseDetailView,
    AdminCourseCreateView,
    AdminCourseUpdateView,
    AdminCourseDeleteView,
)


# =========================================================
# MODULE VIEWS
# =========================================================

from apps.dashboard.views.admin.modules import (

    AdminModuleListView,
    AdminModuleDetailView,
    AdminModuleCreateView,
    AdminModuleUpdateView,
    AdminModuleDeleteView,
)


# =========================================================
# TASK VIEWS
# =========================================================

from apps.dashboard.views.admin.tasks import (

    AdminTaskListView,
    AdminTaskDetailView,
    AdminTaskCreateView,
    AdminTaskUpdateView,
    AdminTaskDeleteView,
)


# =========================================================
# ACTIVITY VIEWS
# =========================================================

from apps.dashboard.views.admin.activities import (

    AdminActivityListView,
    AdminActivityDetailView,
    AdminActivityCreateView,
    AdminActivityUpdateView,
    AdminActivityDeleteView,
)


urlpatterns = [

    # =====================================================
    # COURSES
    # =====================================================

    path(
        'courses/',
        AdminCourseListView.as_view(),
        name='admin_courses'
    ),

    path(
        'courses/create/',
        AdminCourseCreateView.as_view(),
        name='admin_course_create'
    ),

    path(
        'courses/<int:pk>/',
        AdminCourseDetailView.as_view(),
        name='admin_course_detail'
    ),

    path(
        'courses/<int:pk>/edit/',
        AdminCourseUpdateView.as_view(),
        name='admin_course_update'
    ),

    path(
        'courses/<int:pk>/delete/',
        AdminCourseDeleteView.as_view(),
        name='admin_course_delete'
    ),

    # =====================================================
    # MODULES
    # =====================================================

    path(
        'modules/',
        AdminModuleListView.as_view(),
        name='admin_modules'
    ),

    path(
        'modules/create/',
        AdminModuleCreateView.as_view(),
        name='admin_module_create'
    ),

    path(
        'modules/<int:pk>/',
        AdminModuleDetailView.as_view(),
        name='admin_module_detail'
    ),

    path(
        'modules/<int:pk>/edit/',
        AdminModuleUpdateView.as_view(),
        name='admin_module_update'
    ),

    path(
        'modules/<int:pk>/delete/',
        AdminModuleDeleteView.as_view(),
        name='admin_module_delete'
    ),

    # =====================================================
    # TASKS
    # =====================================================

    path(
        'tasks/',
        AdminTaskListView.as_view(),
        name='admin_tasks'
    ),

    path(
        'tasks/create/',
        AdminTaskCreateView.as_view(),
        name='admin_task_create'
    ),

    path(
        'tasks/<int:pk>/',
        AdminTaskDetailView.as_view(),
        name='admin_task_detail'
    ),

    path(
        'tasks/<int:pk>/edit/',
        AdminTaskUpdateView.as_view(),
        name='admin_task_update'
    ),

    path(
        'tasks/<int:pk>/delete/',
        AdminTaskDeleteView.as_view(),
        name='admin_task_delete'
    ),

    # =====================================================
    # ACTIVITIES
    # =====================================================

    path(
        'activities/',
        AdminActivityListView.as_view(),
        name='admin_activities'
    ),

    path(
        'activities/create/',
        AdminActivityCreateView.as_view(),
        name='admin_activity_create'
    ),

    path(
        'activities/<int:pk>/',
        AdminActivityDetailView.as_view(),
        name='admin_activity_detail'
    ),

    path(
        'activities/<int:pk>/edit/',
        AdminActivityUpdateView.as_view(),
        name='admin_activity_update'
    ),

    path(
        'activities/<int:pk>/delete/',
        AdminActivityDeleteView.as_view(),
        name='admin_activity_delete'
    ),
]
