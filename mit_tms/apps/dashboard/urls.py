from django.urls import (
    path,
    include
)

app_name = 'dashboard'

urlpatterns = [

    path(
        '',
        include(
            'apps.dashboard.urls.dashboard_urls'
        )
    ),

    path(
        'admin/',
        include(
            'apps.dashboard.urls.admin_urls'
        )
    ),

    path(
        'student/',
        include(
            'apps.dashboard.urls.student_urls'
        )
    ),

    path(
        'teacher/',
        include(
            'apps.dashboard.urls.teacher_urls'
        )
    ),

    path(
        'staff/',
        include(
            'apps.dashboard.urls.staff_urls'
        )
    ),

    path(
        'parent/',
        include(
            'apps.dashboard.urls.parent_urls'
        )
    ),

    path(
        'alumni/',
        include(
            'apps.dashboard.urls.alumni_urls'
        )
    ),

    path(
        'manage/',
        include(
            'apps.dashboard.urls.crud_urls'
        )
    ),
]
