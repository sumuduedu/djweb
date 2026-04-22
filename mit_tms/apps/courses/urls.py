
from django.urls import path
from .views.course import *
from .views.module import *
from .views.criteria import *
from .views.unit import *
from .views.activity import *
from .views.ajax import *
from .views.task import *
from .views.assessment import *

app_name = "courses"

urlpatterns = [

    # 🔷 Course CRUD

    path('', CourseListView.as_view(), name='course_list'),
    path('course/create/', CourseCreateView.as_view(), name='course_create'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_update'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # 🔥 Module CRUD
    path('modules/add/<int:course_id>/', ModuleCreateView.as_view(), name='module_create'),
    path('modules/<int:pk>/edit/', ModuleUpdateView.as_view(), name='module_update'),
    path('modules/<int:pk>/delete/', ModuleDeleteView.as_view(), name='module_delete'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),


# 🔷 AJAX
path('ajax/get-module-details/', ModuleDetailAjaxView.as_view(), name='get_module_details'),

    # 🔥 Task CRUD
path('tasks/add/<int:module_id>/', TaskCreateView.as_view(), name='task_create'),
path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),
path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),


path('units/add/units/', UnitCreateView.as_view(), name='units_create'),
path('units/add/<int:course_id>/', UnitCreateView.as_view(), name='unit_create'),
path('units/<int:pk>/edit/', UnitUpdateView.as_view(), name='unit_update'),
path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),
path('units/<int:pk>/', UnitDetailView.as_view(), name='unit_detail'),
path('courses/<int:pk>/ncs/', CourseNCSView.as_view(), name='course_ncs'),

path("task/<int:task_id>/activities/", ActivityListView.as_view(), name="activity_list"),
path("task/<int:task_id>/activities/add/", ActivityCreateView.as_view(), name="activity_create"),
path("activity/<int:pk>/edit/", ActivityUpdateView.as_view(), name="activity_update"),
path("activity/<int:pk>/delete/", ActivityDeleteView.as_view(), name="activity_delete"),




# Assessment
path('assessment/add/<int:course_id>/', AssessmentCreateView.as_view(), name='assessment_create'),

# Resource
path('resource/add/<int:course_id>/', ResourceCreateView.as_view(), name='resource_create'),

# Task Assessment
path('task/<int:task_id>/assessment/add/', TaskAssessmentCreateView.as_view(), name='task_assessment_create'),

# Task Standard
path('task/<int:task_id>/standard/add/', TaskStandardCreateView.as_view(), name='task_standard_create'),



# Assessment
path('assessment/<int:pk>/edit/', AssessmentUpdateView.as_view(), name='assessment_update'),
path('assessment/<int:pk>/delete/', AssessmentDeleteView.as_view(), name='assessment_delete'),

# Resource
path('resource/<int:pk>/edit/', ResourceUpdateView.as_view(), name='resource_update'),
path('resource/<int:pk>/delete/', ResourceDeleteView.as_view(), name='resource_delete'),

# Task Assessment
path('task-assessment/<int:pk>/edit/', TaskAssessmentUpdateView.as_view(), name='task_assessment_update'),
path('task-assessment/<int:pk>/delete/', TaskAssessmentDeleteView.as_view(), name='task_assessment_delete'),

# Task Standard
path('task-standard/<int:pk>/edit/', TaskStandardUpdateView.as_view(), name='task_standard_update'),
path('task-standard/<int:pk>/delete/', TaskStandardDeleteView.as_view(), name='task_standard_delete'),

# Criteria
path('criteria/<int:pk>/edit/', CriteriaUpdateView.as_view(), name='criteria_update'),
path('criteria/<int:pk>/delete/', CriteriaDeleteView.as_view(), name='criteria_delete'),


path('element/add/<int:unit_id>/', ElementCreateView.as_view(), name='element_create')
]
