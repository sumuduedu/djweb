from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.core.views import SignupView, ActivateAccountView
from apps.core.forms import CustomLoginForm
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # 🔧 Admin
    path('admin/', admin.site.urls),

    # 🌐 Public Website
    path('', include('apps.website.urls')),

    # 🔐 Auth
    path('login/', auth_views.LoginView.as_view(
        template_name='auth/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),


path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('signup/', SignupView.as_view(), name='signup'),

    # 🔥 ADD THIS (Activation URL)
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

    # 🔗 Allauth (Google etc.)
    path('accounts/', include('allauth.urls')),

    # 📊 Application Modules
    path('app/', include('apps.core.urls')),
    path('app/courses/', include('apps.courses.urls')),
    path('app/batches/', include('apps.batch.urls')),

    # 👤 Custom Accounts App
    path('accounts/custom/', include('apps.accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
