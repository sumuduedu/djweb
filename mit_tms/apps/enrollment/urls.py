# apps/enrollment/urls.py

from django.urls import path
from .views import (
    ApplyStudentView,
    # (optional later)
     ApplyParentView,
    ApplicationListView,
    ApproveApplicationView,
    RejectApplicationView,
    ChangeStudentPasswordView,
)

app_name = "enrollment"


urlpatterns = [
    # ================================
    # 🎓 APPLICATION (USER SIDE)
    # ================================
    path(
        "apply/student/<int:course_id>/",
        ApplyStudentView.as_view(),
        name="apply_student",
    ),

    # 👉 keep this only if you have CBV for parent
     path(
        "apply/parent/<int:course_id>/",
        ApplyParentView.as_view(),
        name="apply_parent",
    ),

    # ================================
    # 📋 APPLICATION MANAGEMENT (ADMIN)
    # ================================
    path(
        "applications/",
        ApplicationListView.as_view(),
        name="application_list",
    ),
    path(
        "applications/<int:pk>/approve/",
        ApproveApplicationView.as_view(),
        name="approve_application",
    ),
    path(
        "applications/<int:pk>/reject/",
        RejectApplicationView.as_view(),
        name="reject_application",
    ),

path(
    'parent/change-student-password/',
    ChangeStudentPasswordView.as_view(),
    name='change_student_password'
)
]
