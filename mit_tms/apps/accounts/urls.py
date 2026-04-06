from django.urls import path
from .views import ProfileView, AccountSettingsView

app_name = "accounts"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("settings/", AccountSettingsView.as_view(), name="account_settings"),
]
