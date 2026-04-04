from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


# Home page
class HomeView(TemplateView):
    template_name = "website/home.html"


# Dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"


# Signup
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')
