from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ================= ADMIN =================
    path('admin/', admin.site.urls),

    # ================= PUBLIC WEBSITE =================
    path('', include('apps.website.urls')),
    path('careers/', include('apps.careers.urls')),

    # ================= ACCOUNTS =================
    path('accounts/', include('apps.accounts.urls')),
    path('auth/', include('allauth.urls')),  # social login

    # ================= APPLICATION =================
    path('app/', include([
        path('', include('apps.dashboard.urls')),              # 👉 dashboard should be here
        path('courses/', include('apps.courses.urls')),
        path('batches/', include('apps.batch.urls')),
        path('enrollment/', include('apps.enrollment.urls')),
        path('schedule/', include('apps.scheduling.urls')),
        path('lessons/', include('apps.lessonplan.urls')),
        path('core/', include('apps.core.urls')),
    ])),
]


# ================= MEDIA =================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
