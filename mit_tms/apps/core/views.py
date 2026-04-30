from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Profile


class HomeView(TemplateView):
    template_name = "website/home.html"


ROLE_REDIRECTS = {
    'ADMIN': 'dashboard:admin_dashboard',
    'STAFF': 'dashboard:staff_dashboard',
    'TEACHER': 'dashboard:teacher_dashboard',
    'STUDENT': 'dashboard:student_dashboard',
    'PARENT': 'dashboard:parent_dashboard',
    'ALUMNI': 'dashboard:alumni_dashboard',
}


@login_required
def dashboard_redirect(request):
    profile = request.user.profile
    redirect_url = ROLE_REDIRECTS.get(profile.role, 'dashboard:guest_dashboard')
    return redirect(redirect_url)
