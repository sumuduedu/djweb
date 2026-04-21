from django.urls import path
from .views import notification_api
from .views import (
    ApplyView,
    ApplicationListView,
    ApproveApplicationView,
    RejectApplicationView,
)

app_name = "enrollment"

urlpatterns = [
    path("apply/<int:course_id>/", ApplyView.as_view(), name="apply"),

    path("applications/", ApplicationListView.as_view(), name="application_list"),
    path("applications/<int:pk>/approve/", ApproveApplicationView.as_view(), name="approve_application"),
    path("applications/<int:pk>/reject/", RejectApplicationView.as_view(), name="reject_application"),
    path(
    "notifications/",
    notification_api,
    name="notifications_api",
),
]
