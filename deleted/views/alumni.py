from .base import BaseView
from apps.core.gateway import get_student_enrollments


class AlumniDashboardView(BaseView):
    allowed_roles = ['ALUMNI']
    template_name = "dashboard/alumni.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['enrollments'] = get_student_enrollments(self.request.user)

        return context

from django.views.generic import TemplateView


class AlumniJobsView(TemplateView):
    template_name = "core/alumni/jobs.html"


from django.views.generic import TemplateView


class AlumniEventsView(TemplateView):
    template_name = "core/alumni/events.html"

from django.views.generic import TemplateView


class AlumniNetworkView(TemplateView):
    template_name = "core/alumni/network.html"

from django.views.generic import TemplateView


class AlumniCertificatesView(TemplateView):
    template_name = "core/alumni/certificates.html"
