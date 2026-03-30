from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Home page
class HomeView(TemplateView):
    template_name = "core/home.html"


# Dashboard (LOGIN REQUIRED)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
