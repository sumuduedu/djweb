from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from apps.core.views import SignupView, ActivateAccountView
from apps.core.forms import CustomLoginForm


urlpatterns = [

    # ================= ADMIN =================
    path('admin/', admin.site.urls),

    # ================= PUBLIC WEBSITE =================
    path('', include('apps.website.urls')),


    # ================= AUTH =================

    # 🔐 Login (your custom UI)
    path('login/', auth_views.LoginView.as_view(
        template_name='auth/login.html',
        authentication_form=CustomLoginForm,
        redirect_authenticated_user=True
    ), name='login'),

    # 🔓 Logout
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # 🆕 Signup
    path('signup/', SignupView.as_view(), name='signup'),

    # 📧 Email activation
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),


    # ================= APPLICATION =================

    # Core (dashboard, redirect)
    path('app/', include('apps.core.urls')),

    # Courses
    path('app/courses/', include('apps.courses.urls')),

    # Batches
    path('app/batches/', include('apps.batch.urls')),

    # Custom account management (profile, users)
    path('accounts/', include('apps.accounts.urls')),


    # ================= OPTIONAL (ONLY IF USING GOOGLE) =================
    # ⚠️ Keep this ONLY if you configured allauth properly
    path('auth/', include('allauth.urls')),


]


# ================= MEDIA =================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
