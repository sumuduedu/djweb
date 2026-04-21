from django.urls import path
from .views import *


app_name = "courses"

urlpatterns = [

    # 🔷 Course CRUD
    path('', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # 🔥 Module CRUD
    path('modules/add/<int:course_id>/', ModuleCreateView.as_view(), name='module_create'),
    path('modules/<int:pk>/edit/', ModuleUpdateView.as_view(), name='module_update'),
    path('modules/<int:pk>/delete/', ModuleDeleteView.as_view(), name='module_delete'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),


# 🔷 AJAX
path('ajax/get-module-details/', get_module_details, name='get_module_details'),

    # 🔥 Task CRUD
path('tasks/add/<int:module_id>/', TaskCreateView.as_view(), name='task_create'),
path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),
path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),



path('units/add/<int:course_id>/', UnitCreateView.as_view(), name='unit_create'),
path('units/<int:pk>/edit/', UnitUpdateView.as_view(), name='unit_update'),
path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),
path('units/<int:pk>/', UnitDetailView.as_view(), name='unit_detail'),
path('courses/<int:pk>/ncs/', CourseNCSView.as_view(), name='course_ncs'),

path("task/<int:task_id>/activities/", ActivityListView.as_view(), name="activity_list"),
path("task/<int:task_id>/activities/add/", ActivityCreateView.as_view(), name="activity_create"),
path("activity/<int:pk>/edit/", ActivityUpdateView.as_view(), name="activity_update"),
path("activity/<int:pk>/delete/", ActivityDeleteView.as_view(), name="activity_delete"),
]
