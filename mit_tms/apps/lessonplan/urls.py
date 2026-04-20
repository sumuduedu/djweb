from django.urls import path
from .views import (
    LessonListView,
    LessonCreateView,
    LessonDetailView,
    LessonUpdateView,
    LessonDeleteView
)

app_name = "lessonplan"

urlpatterns = [
    path("", LessonListView.as_view(), name="list"),
    path("create/", LessonCreateView.as_view(), name="create"),
    path("<int:pk>/", LessonDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", LessonUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", LessonDeleteView.as_view(), name="delete"),
]
