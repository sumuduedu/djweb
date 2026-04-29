from django.db import models
from django.contrib.auth.models import User


# ================================
# 🔷 COMMON BASE MODEL (SAFE ADD)
# ================================
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ================================
# 🔷 PROFILE (ROLE SYSTEM)
# ================================
class Profile(TimeStampedModel):

    # ✅ SAFE CONSTANTS (no breaking)
    ROLE_ADMIN = 'ADMIN'
    ROLE_STAFF = 'STAFF'
    ROLE_TEACHER = 'TEACHER'
    ROLE_STUDENT = 'STUDENT'
    ROLE_ALUMNI = 'ALUMNI'
    ROLE_PARENT = 'PARENT'
    ROLE_GUEST = 'GUEST'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_STAFF, 'Staff'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_STUDENT, 'Student'),
        (ROLE_ALUMNI, 'Alumni'),
        (ROLE_PARENT, 'Parent'),
        (ROLE_GUEST, 'Guest'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_GUEST
    )

    image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ================================
# 🔷 BASE PERSON (SAFE ADD)
# ================================
class BasePerson(TimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # ✅ SAFE ADD (no break)
    is_active = models.BooleanField(default=True)

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        abstract = True


# ================================
# 🎓 STUDENT MODEL
# ================================
class Student(BasePerson):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student"
    )

    # ❗ KEPT (no breaking)
    full_name = models.CharField(max_length=255)

    parents = models.ManyToManyField(
        'Parent',
        related_name='students',
        blank=True
    )

    def __str__(self):
        return self.full_name or self.get_full_name()


# ================================
# 👨‍🏫 TEACHER MODEL
# ================================
class Teacher(BasePerson):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher"
    )

    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name or self.get_full_name()


# ================================
# 🧑‍💼 STAFF MODEL
# ================================
class Staff(BasePerson):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff"
    )

    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name or self.get_full_name()


# ================================
# 👨‍👩‍👧 PARENT MODEL
# ================================
class Parent(BasePerson):

    RELATION_CHOICES = (
        ('FATHER', 'Father'),
        ('MOTHER', 'Mother'),
        ('GUARDIAN', 'Guardian'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="parent"
    )

    relationship = models.CharField(
        max_length=20,
        choices=RELATION_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


# ================================
# 🎓 ALUMNI MODEL
# ================================
class Alumni(BasePerson):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="alumni"
    )

    job_title = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.get_full_name()
