from django.db import models
from django.contrib.auth.models import User


# ================================
# 🔷 PROFILE (ROLE SYSTEM)
# ================================
class Profile(models.Model):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
        ('ALUMNI', 'Alumni'),
        ('PARENT', 'Parent'),
        ('GUEST', 'Guest'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='GUEST'   # 🔥 DEFAULT ROLE
    )

    image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ================================
# 🎓 STUDENT MODEL
# ================================
class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student"
    )

    full_name = models.CharField(max_length=255)

    # 🔥 MANY PARENTS
    parents = models.ManyToManyField(
        'Parent',
        related_name='students',
        blank=True
    )

    def __str__(self):
        return self.full_name


# ================================
# 👨‍🏫 TEACHER MODEL
# ================================
class Teacher(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher"
    )

    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


# ================================
# 🧑‍💼 STAFF MODEL
# ================================
class Staff(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff"
    )

    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


# ================================
# 👨‍👩‍👧 PARENT MODEL
# ================================
class Parent(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="parent"
    )

    relationship = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    def __str__(self):
        return self.user.username

class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
