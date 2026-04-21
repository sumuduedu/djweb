from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ================= ADMIN =================
    path('admin/', admin.site.urls),

    # ================= PUBLIC WEBSITE =================
    path('', include('apps.website.urls')),
    path("careers/", include("apps.careers.urls")),


    # ================= ACCOUNTS (AUTH + PROFILE) =================
    path('accounts/', include('apps.accounts.urls')),

    # ================= APPLICATION =================
    path('app/', include('apps.core.urls')),
    path('app/courses/', include('apps.courses.urls')),

    path('app/batches/', include('apps.batch.urls')),
    path('app/enrollment/', include('apps.enrollment.urls')),
    path('app/schedule/', include('apps.scheduling.urls')),
    # mit_tms/urls.py
    path("app/lessons/", include("apps.lessonplan.urls", namespace="lessonplan")),



    # ================= OPTIONAL =================
    path('auth/', include('allauth.urls')),  # only if used

]


# ================= MEDIA =================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

