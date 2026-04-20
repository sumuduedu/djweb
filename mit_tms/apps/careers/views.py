from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Job, Company, Application


# ========================
# 🏠 HOME
# ========================
class CareerHubHomeView(TemplateView):
    template_name = "careers/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jobs"] = Job.objects.filter(is_active=True)[:6]
        context["companies"] = Company.objects.all()[:6]
        return context


# ========================
# 💼 JOB LIST
# ========================
class JobListView(ListView):
    model = Job
    template_name = "careers/job_list.html"
    context_object_name = "jobs"
    paginate_by = 10

    def get_queryset(self):
        return Job.objects.filter(is_active=True).select_related("company")


# ========================
# 📄 JOB DETAIL
# ========================
class JobDetailView(DetailView):
    model = Job
    template_name = "careers/job_detail.html"
    context_object_name = "job"


# ========================
# 📝 APPLY JOB
# ========================
class ApplyJobView(LoginRequiredMixin, CreateView):
    model = Application
    fields = ["cv", "cover_letter"]
    template_name = "careers/apply_job.html"

    def form_valid(self, form):
        job = get_object_or_404(Job, pk=self.kwargs["pk"])

        # prevent duplicate apply
        if Application.objects.filter(user=self.request.user, job=job).exists():
            messages.warning(self.request, "You already applied.")
            return redirect("careers:job_detail", pk=job.pk)

        form.instance.user = self.request.user
        form.instance.job = job

        messages.success(self.request, "Application submitted.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.job.get_absolute_url() if hasattr(self.object.job, "get_absolute_url") else "/careers/jobs/"


# ========================
# 🏢 COMPANY LIST
# ========================
class EmployerListView(ListView):
    model = Company
    template_name = "careers/employer_list.html"
    context_object_name = "companies"


class EmployerDetailView(DetailView):
    model = Company
    template_name = "careers/employer_detail.html"
    context_object_name = "company"


# ========================
# 📄 MY APPLICATIONS
# ========================
class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "careers/my_applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related("job", "job__company")


# ========================
# ❤️ SAVED JOBS (optional placeholder)
# ========================
class SavedJobsView(LoginRequiredMixin, TemplateView):
    template_name = "careers/saved_jobs.html"


# ========================
# 🧑‍💼 EMPLOYER DASHBOARD
# ========================
class EmployerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "careers/dashboard.html"

from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages

from .models import Job, Company

class EmployerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "careers/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company = self.get_company()

        context["jobs"] = Job.objects.filter(company=company)
        context["total_jobs"] = context["jobs"].count()
        context["total_applications"] = sum(
            job.applications.count() for job in context["jobs"]
        )

        return context

    def get_company(self):
        # Assumption: user is linked to a company
        return get_object_or_404(Company, email=self.request.user.email)

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ["title", "description", "location", "job_type", "salary", "deadline"]
    template_name = "careers/job_form.html"
    success_url = reverse_lazy("careers:dashboard")

    def form_valid(self, form):
        company = self.get_company()
        form.instance.company = company

        messages.success(self.request, "Job posted successfully.")
        return super().form_valid(form)

    def get_company(self):
        return get_object_or_404(Company, email=self.request.user.email)

class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    fields = ["title", "description", "location", "job_type", "salary", "deadline", "is_active"]
    template_name = "careers/job_form.html"
    success_url = reverse_lazy("careers:dashboard")

    def get_queryset(self):
        company = self.get_company()
        return Job.objects.filter(company=company)

    def form_valid(self, form):
        messages.success(self.request, "Job updated successfully.")
        return super().form_valid(form)

    def get_company(self):
        return get_object_or_404(Company, email=self.request.user.email)

from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import StudentProfile


# 📝 Create / Update CV Profile
class StudentProfileView(LoginRequiredMixin, UpdateView):
    model = StudentProfile
    fields = ["full_name", "bio", "skills", "experience", "cv", "is_public"]
    template_name = "careers/student_profile.html"
    success_url = reverse_lazy("careers:profile")

    def get_object(self):
        profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        return profile
from django.views.generic import ListView
from .models import StudentProfile


from django.db.models import Q
from django.db.models import Q
from django.views.generic import ListView
from .models import StudentProfile


class StudentListView(ListView):
    model = StudentProfile
    template_name = "careers/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        queryset = StudentProfile.objects.filter(is_public=True)

        q = self.request.GET.get("q")
        exp = self.request.GET.get("experience")

        if q:
            queryset = queryset.filter(
                Q(skills__icontains=q) |
                Q(bio__icontains=q)
            )

        if exp:
            queryset = queryset.filter(
                experience__icontains=exp
            )

        # 🔥 IMPORTANT FIX (add this)
        for student in queryset:
            student.skills_list = [
                s.strip().title()
                for s in (student.skills or "").split(",")
                if s.strip()
            ]

        return queryset
from django.views.generic import DetailView
from .models import StudentProfile

class StudentDetailView(DetailView):
    model = StudentProfile
    template_name = "careers/student_detail.html"
    context_object_name = "student"
