from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# =========================
# 🏢 COMPANY
# =========================
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="companies/", blank=True, null=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# 💼 JOB
# =========================
class Job(models.Model):

    JOB_TYPE = (
        ("FULL_TIME", "Full Time"),
        ("PART_TIME", "Part Time"),
        ("INTERNSHIP", "Internship"),
    )

    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")

    description = models.TextField()
    location = models.CharField(max_length=255)

    job_type = models.CharField(max_length=20, choices=JOB_TYPE)
    salary = models.CharField(max_length=100, blank=True)

    deadline = models.DateField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("careers:job_detail", args=[self.id])

    class Meta:
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["job_type"]),
        ]


# =========================
# 👨‍🎓 STUDENT PROFILE (CV SYSTEM)
# =========================
from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    skills = models.TextField(
        help_text="Comma separated skills (e.g. Python, Excel)"
    )

    # 🔥 Structured profile fields
    education = models.TextField(blank=True)
    training = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    # 📄 CV
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)

    # 🌐 Visibility
    is_public = models.BooleanField(default=True)

    # 🕒 Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# =========================
# 📄 JOB APPLICATION
# =========================
class Application(models.Model):

    STATUS = (
        ("APPLIED", "Applied"),
        ("SHORTLISTED", "Shortlisted"),
        ("REJECTED", "Rejected"),
        ("HIRED", "Hired"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")

    # 🔥 NOTE: CV is optional now (use StudentProfile CV by default)
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)

    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="APPLIED")

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user} → {self.job}"
