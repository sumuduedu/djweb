from django.urls import path
from .views import (
    LessonListView,
    LessonCreateView,
    LessonDetailView,
    LessonUpdateView,
    LessonDeleteView,
    GenerateLessonView,
    LoadTasksView,
    LessonBuilderView,          # ✅ NEW
    UpdateActivityOrderView,     # ✅ NEW
    LessonPrintView,
)

app_name = "lessonplan"

urlpatterns = [
    path("", LessonListView.as_view(), name="list"),
    path("create/", LessonCreateView.as_view(), name="create"),
    path("<int:pk>/", LessonDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", LessonUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", LessonDeleteView.as_view(), name="delete"),

    path("generate/<int:task_id>/", GenerateLessonView.as_view(), name="generate"),

    # AJAX
    path("ajax/load-tasks/", LoadTasksView.as_view(), name="ajax_load_tasks"),

    # 🔥 NEW (Drag & Drop Builder)
    path("<int:pk>/builder/", LessonBuilderView.as_view(), name="builder"),

    # 🔥 NEW (AJAX save order)
    path("update-order/", UpdateActivityOrderView.as_view(), name="update_order"),
    path("<int:pk>/print/", LessonPrintView.as_view(), name="print"),
    path("ajax/load-tasks/", LoadTasksView.as_view(), name="ajax_load_tasks")
]
