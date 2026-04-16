from django.urls import path
from .views import *

app_name = "batch"

urlpatterns = [
    path("", BatchListView.as_view(), name="batch_list"),
    path("create/", BatchCreateView.as_view(), name="batch_create"),
    path("<int:pk>/", BatchDetailView.as_view(), name="batch_detail"),
    path("<int:pk>/update/", BatchUpdateView.as_view(), name="batch_update"),
    path("<int:pk>/delete/", BatchDeleteView.as_view(), name="batch_delete"),

    path("<int:batch_id>/assign-student/<int:student_id>/",
         AssignStudentToBatchView.as_view(), name="assign_student"),

    path("<int:batch_id>/assign-teacher/",
         AssignTeacherView.as_view(), name="assign_teacher"),
]
