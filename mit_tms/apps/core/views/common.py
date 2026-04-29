from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Profile


class HomeView(TemplateView):
    template_name = "website/home.html"


ROLE_REDIRECTS = {
    'ADMIN': 'core:admin_dashboard',
    'STAFF': 'core:staff_dashboard',
    'TEACHER': 'core:teacher_dashboard',
    'STUDENT': 'core:student_dashboard',
    'PARENT': 'core:parent_dashboard',
    'ALUMNI': 'core:alumni_dashboard',
}


@login_required
def dashboard_redirect(request):
    profile = request.user.profile
    redirect_url = ROLE_REDIRECTS.get(profile.role, 'core:guest_dashboard')
    return redirect(redirect_url)
