# ================================
# IMPORTS
# ================================
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from apps.accounts.models import Profile

# Import views (ONLY ONCE)
from .base import *
from .admin import *
from .student import *
from .teacher import *
from .staff import *
from .parent import *
from .alumni import *
from .guest import *


# ================================
# HOME VIEW
# ================================
class HomeView(TemplateView):
    template_name = "website/home.html"


# ================================
# ROLE → DASHBOARD MAP
# ================================
ROLE_REDIRECTS = {
    'ADMIN': 'dashboard:admin_dashboard',
    'STAFF': 'dashboard:staff_dashboard',
    'TEACHER': 'dashboard:teacher_dashboard',
    'STUDENT': 'dashboard:student_dashboard',
    'PARENT': 'dashboard:parent_dashboard',
    'ALUMNI': 'dashboard:alumni_dashboard',
}


# ================================
# DASHBOARD REDIRECT
# ================================
@login_required
def dashboard_redirect(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    redirect_url = ROLE_REDIRECTS.get(
        profile.role,
        'dashboard:guest_dashboard'  # fallback
    )

    return redirect(redirect_url)
