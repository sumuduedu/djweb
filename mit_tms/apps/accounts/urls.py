from django.urls import path
from .views import (
    CustomLoginView,
    logout_view,
    SignupView,
    ActivateAccountView,
    ProfileView,
    AccountSettingsView,
    UserListView,
    UserCreateView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
    ToggleUserStatusView,
)

app_name = "accounts"

urlpatterns = [
    # 🔐 AUTH
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    path(
    'users/<int:pk>/toggle/',
    ToggleUserStatusView.as_view(),
    name='user_toggle',
),

    # 👤 PROFILE
    path("profile/", ProfileView.as_view(), name="profile"),

    # ⚙️ SETTINGS
    path("settings/", AccountSettingsView.as_view(), name="account_settings"),

    # 👥 USER MANAGEMENT
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/create/", UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
]
