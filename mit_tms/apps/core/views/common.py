from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Profile


class HomeView(TemplateView):
    template_name = "website/home.html"


@login_required
def dashboard_redirect(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.role == 'ADMIN':
        return redirect('core:admin_dashboard')
    elif profile.role == 'STAFF':
        return redirect('core:staff_dashboard')
    elif profile.role == 'TEACHER':
        return redirect('core:teacher_dashboard')
    elif profile.role == 'STUDENT':
        return redirect('core:student_dashboard')
    elif profile.role == 'PARENT':
        return redirect('core:parent_dashboard')
    elif profile.role == 'ALUMNI':
        return redirect('core:alumni_dashboard')

    return redirect('core:guest_dashboard')
