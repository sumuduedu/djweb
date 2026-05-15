from django.urls import path

from apps.dashboard.views.alumni.profile import (
    AlumniProfileView
)

from apps.dashboard.views.alumni.courses import (
    AlumniCoursesView
)

# from apps.dashboard.views.alumni.certificates import (
#     AlumniCertificatesView
# )
#
# from apps.dashboard.views.alumni.employment import (
#     AlumniEmploymentView
# )
#
# from apps.dashboard.views.alumni.networking import (
#     AlumniNetworkingView
# )
#
# from apps.dashboard.views.alumni.messages import (
#     AlumniMessagesView
# )
#
# from apps.dashboard.views.alumni.settings import (
#     AlumniSettingsView
# )


urlpatterns = [

    path(
        'profile/',
        AlumniProfileView.as_view(),
        name='alumni_profile'
    ),

    path(
        'courses/',
        AlumniCoursesView.as_view(),
        name='alumni_courses'
    ),
    #
    # path(
    #     'certificates/',
    #     AlumniCertificatesView.as_view(),
    #     name='alumni_certificates'
    # ),
    #
    # path(
    #     'employment/',
    #     AlumniEmploymentView.as_view(),
    #     name='alumni_employment'
    # ),
    #
    # path(
    #     'networking/',
    #     AlumniNetworkingView.as_view(),
    #     name='alumni_networking'
    # ),
    #
    # path(
    #     'messages/',
    #     AlumniMessagesView.as_view(),
    #     name='alumni_messages'
    # ),
    #
    # path(
    #     'settings/',
    #     AlumniSettingsView.as_view(),
    #     name='alumni_settings'
    # ),
]
