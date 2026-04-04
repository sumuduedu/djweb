from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.core.views import SignupView   # ✅ ADD THIS

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🌐 Public Website
    path('', include('apps.website.urls')),

    # 🔐 Application (Dashboard)
    path('app/', include('apps.core.urls')),

    # 📚 Course Management (inside app)
    path('app/courses/', include('apps.courses.urls')),

    # 🔑 Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='auth/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/', SignupView.as_view(), name='signup'),   # ✅ ADD THIS

    path('accounts/', include('allauth.urls')),
]
