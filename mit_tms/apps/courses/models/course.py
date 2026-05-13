from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .base import BaseModel


class Course(BaseModel):

    # =====================================================
    # 🔷 CHOICES
    # =====================================================
    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    DELIVERY_MODE_CHOICES = [
        ('CLASSROOM', 'Classroom'),
        ('ONLINE', 'Online'),
        ('BLENDED', 'Blended'),
    ]

    COURSE_MODE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
    ]

    CURRICULUM_CATEGORY_CHOICES = [
        ('NVQ', 'NVQ'),
        ('NON_NVQ', 'Non-NVQ'),
    ]

    MEDIUM_CHOICES = [
        ('SINHALA', 'Sinhala'),
        ('ENGLISH', 'English'),
        ('TAMIL', 'Tamil'),
    ]

    AVAILABILITY_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('UNAVAILABLE', 'Unavailable'),
    ]

    ENTRY_QUALIFICATION_CHOICES = [
        ('UPTO_OL', 'Upto O/L'),
        ('AL', 'A/L'),
        ('DIPLOMA', 'Diploma'),
        ('DEGREE', 'Degree'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    # =====================================================
    # 🔷 BASIC INFO
    # =====================================================
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True,null=True, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, null=True)

    # =====================================================
    # 🔷 ACADEMIC STRUCTURE
    # =====================================================
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    entry_qualification = models.CharField(
        max_length=20,
        choices=ENTRY_QUALIFICATION_CHOICES,
        blank=True
    )

    curriculum_category = models.CharField(
        max_length=20,
        choices=CURRICULUM_CATEGORY_CHOICES,
        default='NON_NVQ'
    )

    curriculum_availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='AVAILABLE'
    )

    equivalent_course = models.CharField(max_length=100, blank=True)

    # =====================================================
    # 🔷 DELIVERY
    # =====================================================
    delivery_mode = models.CharField(
        max_length=20,
        choices=DELIVERY_MODE_CHOICES,
        default='CLASSROOM'
    )

    course_mode = models.CharField(
        max_length=20,
        choices=COURSE_MODE_CHOICES,
        default='PART_TIME'
    )

    medium = models.CharField(
        max_length=20,
        choices=MEDIUM_CHOICES,
        default='SINHALA'
    )

    # =====================================================
    # 🔷 DURATION & HOURS
    # =====================================================
    duration_months = models.PositiveIntegerField(default=0)

    theory_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    practical_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    assignment_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    ojt_months = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    # =====================================================
    # 🔷 CAPACITY
    # =====================================================
    batches_per_year = models.IntegerField(default=1)
    students_per_batch = models.IntegerField(default=0)

    # =====================================================
    # 🔷 FINANCIAL
    # =====================================================
    course_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_free = models.BooleanField(default=False)

    fee_includes = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g. registration, certification"
    )

    # =====================================================
    # 🔷 RESOURCES
    # =====================================================
    tools_available = models.TextField(blank=True)
    equipment_available = models.TextField(blank=True)
    machinery_available = models.TextField(blank=True)

    # =====================================================
    # 🔷 NVQ
    # =====================================================
    nvq_level = models.IntegerField(null=True, blank=True)
    qualification_code = models.CharField(max_length=50, blank=True)

    ncs = models.ForeignKey(
        'courses.NCS',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    # =====================================================
    # 🔷 PEDAGOGY
    # =====================================================
    prerequisite = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)

    # =====================================================
    # 🔷 SYSTEM
    # =====================================================
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')

    # =====================================================
    # 🔥 CALCULATED FIELD
    # =====================================================
    @property
    def total_hours(self):
        return (
            (self.theory_hours or 0) +
            (self.practical_hours or 0) +
            (self.assignment_hours or 0)
        )

    # =====================================================
    # 🔷 VALIDATION
    # =====================================================
    def clean(self):
        if self.is_free and self.course_fee:
            raise ValidationError("Free courses should not have a fee")

    # =====================================================
    # 🔷 AUTO SLUG
    # =====================================================
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.title}"
