from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    FileExtensionValidator,
    RegexValidator
)
from django.core.exceptions import ValidationError


# =========================================================
# 🔷 COMMON BASE MODEL
# =========================================================

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


# =========================================================
# 🔷 PROFILE MODEL
# =========================================================

class Profile(TimeStampedModel):

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
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_GUEST,
        db_index=True
    )

    image = models.ImageField(
        upload_to='profiles/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'jpg',
                    'jpeg',
                    'png'
                ]
            )
        ],
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['user__username']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def clean(self):

        valid_roles = [
            choice[0]
            for choice in self.ROLE_CHOICES
        ]

        if self.role not in valid_roles:
            raise ValidationError(
                "Invalid role selected"
            )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# =========================================================
# 🔷 ABSTRACT BASE PERSON
# =========================================================

class BasePerson(TimeStampedModel):

    phone_validator = RegexValidator(
        regex=r'^[0-9+\\- ]+$',
        message='Invalid phone number'
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone_number = models.CharField(
        max_length=20,
        validators=[phone_validator],
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    class Meta:
        abstract = True

    def get_full_name(self):

        full_name = self.user.get_full_name()

        if full_name:
            return full_name

        return self.user.username


# =========================================================
# 🎓 STUDENT MODEL
# =========================================================

class Student(BasePerson):

    full_name = models.CharField(
        max_length=255
    )

    student_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    admission_date = models.DateField(
        blank=True,
        null=True
    )

    parents = models.ManyToManyField(
        'Parent',
        related_name='students',
        blank=True
    )

    class Meta:
        ordering = ['student_id']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def clean(self):

        if hasattr(self.user, 'teacher'):
            raise ValidationError(
                'User already assigned as Teacher'
            )

    def __str__(self):
        return self.full_name or self.get_full_name()


# =========================================================
# 👨‍🏫 TEACHER MODEL
# =========================================================

class Teacher(BasePerson):

    full_name = models.CharField(
        max_length=255
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    specialization = models.CharField(
        max_length=255,
        blank=True
    )

    qualification = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def clean(self):

        if hasattr(self.user, 'student'):
            raise ValidationError(
                'User already assigned as Student'
            )

    def __str__(self):
        return self.full_name or self.get_full_name()


# =========================================================
# 🧑‍💼 STAFF MODEL
# =========================================================

class Staff(BasePerson):

    full_name = models.CharField(
        max_length=255
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    department = models.CharField(
        max_length=255,
        blank=True
    )

    designation = models.CharField(
        max_length=255,
        blank=True
    )

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

    def __str__(self):
        return self.full_name or self.get_full_name()


# =========================================================
# 👨‍👩‍👧 PARENT MODEL
# =========================================================

class Parent(BasePerson):

    RELATION_FATHER = 'FATHER'
    RELATION_MOTHER = 'MOTHER'
    RELATION_GUARDIAN = 'GUARDIAN'

    RELATION_CHOICES = (
        (RELATION_FATHER, 'Father'),
        (RELATION_MOTHER, 'Mother'),
        (RELATION_GUARDIAN, 'Guardian'),
    )

    relationship = models.CharField(
        max_length=20,
        choices=RELATION_CHOICES,
        blank=True,
        null=True
    )

    occupation = models.CharField(
        max_length=255,
        blank=True
    )

    emergency_contact = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'

    def __str__(self):
        return self.get_full_name()


# =========================================================
# 🎓 ALUMNI MODEL
# =========================================================

class Alumni(BasePerson):

    graduation_year = models.IntegerField(
        blank=True,
        null=True
    )

    company = models.CharField(
        max_length=255,
        blank=True
    )

    job_title = models.CharField(
        max_length=255,
        blank=True
    )

    linkedin = models.URLField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Alumni'
        verbose_name_plural = 'Alumni'

    def __str__(self):
        return self.get_full_name()
