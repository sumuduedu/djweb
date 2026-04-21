from django.urls import path
from . import views

app_name = "careers"

urlpatterns = [

    # 🌐 HOME
    path("", views.CareerHubHomeView.as_view(), name="home"),

    # =====================
    # 💼 JOBS
    # =====================
    path("jobs/", views.JobListView.as_view(), name="job_list"),
    path("jobs/create/", views.JobCreateView.as_view(), name="job_create"),
    path("jobs/<int:pk>/", views.JobDetailView.as_view(), name="job_detail"),
    path("jobs/<int:pk>/apply/", views.ApplyJobView.as_view(), name="apply_job"),
    path("jobs/<int:pk>/edit/", views.JobUpdateView.as_view(), name="job_edit"),

    # =====================
    # 🏢 EMPLOYERS
    # =====================
    path("employers/", views.EmployerListView.as_view(), name="employer_list"),
    path("employers/<int:pk>/", views.EmployerDetailView.as_view(), name="employer_detail"),
    path("dashboard/", views.EmployerDashboardView.as_view(), name="dashboard"),

    # =====================
    # 📄 APPLICATIONS
    # =====================
    path("applications/", views.MyApplicationsView.as_view(), name="my_applications"),
    path("saved/", views.SavedJobsView.as_view(), name="saved_jobs"),

    # =====================
    # 👨‍🎓 STUDENTS / TALENT
    # =====================
    path("profile/", views.StudentProfileView.as_view(), name="profile"),
    path("talents/", views.StudentListView.as_view(), name="student_list"),
    path("talents/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),

]
