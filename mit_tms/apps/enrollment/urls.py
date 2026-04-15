from django.urls import path
from .views import enroll_view
from apps.enrollment.views import apply_student, apply_teacher, apply_parent
urlpatterns = [
    path("enroll/<int:batch_id>/", enroll_view, name="enroll"),
]
