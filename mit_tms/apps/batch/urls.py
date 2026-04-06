from django.urls import path
from .views import *

app_name = 'batch'

urlpatterns = [

    # =====================================================
    # 🔷 Batch CRUD
    # =====================================================
    path('batches/', BatchListView.as_view(), name='batch_list'),
    path('batches/create/', BatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch_detail'),
    path('batches/<int:pk>/edit/', BatchUpdateView.as_view(), name='batch_update'),
    path('batches/<int:pk>/delete/', BatchDeleteView.as_view(), name='batch_delete'),

    # =====================================================
    # 🔷 Module Plan
    # =====================================================
    path('batches/<int:batch_id>/plans/add/', ModulePlanCreateView.as_view(), name='module_plan_create'),

    # =====================================================
    # 🔷 Timetable Generate
    # =====================================================
    path('batches/<int:pk>/generate/', generate_timetable_view, name='generate_timetable'),

    # =====================================================
    # 🔷 Gantt UI
    # =====================================================
    path('gantt/', GanttView.as_view(), name='gantt'),

    # =====================================================
    # 🔷 API (Drag & Drop System)
    # =====================================================
    path('api/modules/<int:batch_id>/', load_modules, name='load_modules'),
    path('api/save/', save_timetable, name='save_timetable'),
    path('api/load/', load_timetable, name='load_timetable'),

    # =====================================================
    # 🔷 Timetable CRUD (ORIGINAL)
    # =====================================================
    path('', TimetableListView.as_view(), name='list'),
    path('add/', TimetableCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', TimetableUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', TimetableDeleteView.as_view(), name='delete'),

    # =====================================================
    # 🔥 ADDED ALIASES (DO NOT REMOVE ORIGINAL)
    # =====================================================
    path('timetable/', TimetableListView.as_view(), name='timetable_list'),
    path('timetable/add/', TimetableCreateView.as_view(), name='timetable_add'),
    path('timetable/edit/<int:pk>/', TimetableUpdateView.as_view(), name='timetable_edit'),
    path('timetable/delete/<int:pk>/', TimetableDeleteView.as_view(), name='timetable_delete'),
]
