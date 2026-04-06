from django.db import models
from django.contrib.auth.models import User


# ================================
# 🔷 PROFILE (CORE ROLE SYSTEM)
# ================================
class Profile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')

    # 🔥 ADD THIS
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# ================================
# 🎓 STUDENT MODEL
# ================================
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


# ================================
# 👨‍🏫 TEACHER MODEL
# ================================
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher")
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name
