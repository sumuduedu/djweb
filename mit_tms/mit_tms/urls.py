from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.core.views import SignupView   # ✅ ADD THIS
from django.conf import settings
from django.conf.urls.static import static
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

        path('app/batches/', include('apps.batch.urls')),   # 👈 ADD THIS
            path("accounts/", include("apps.accounts.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
