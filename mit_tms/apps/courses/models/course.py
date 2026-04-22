from django.db import models
from django.conf import settings
from .base import BaseModel

# course.py
from .resource import PhysicalResource
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

    INDUSTRY_SECTORS = [
    ("A", "Agriculture, Hunting and Forestry"),
    ("B", "Fishing"),
    ("BCS", "Common"),
    ("C", "Mining and Quarrying"),
    ("D", "Manufacturing"),
    ("E", "Electricity, Gas and Water Supply"),
    ("F", "Construction"),
    ("G", "Wholesale and Retail Trade"),
    ("H", "Hotel and Restaurants"),
    ("I", "Transport, Storage and Communications"),
    ("J", "Financial Intermediation"),
    ("K", "Real Estate, Renting and Business Activities"),
    ("L", "Public Administration and Defense"),
    ("M", "Education"),
    ("N", "Health and Social Work"),
    ("O", "Other Community, Social and Personal Service Activities"),
    ("P", "Private Households with Employed Persons"),
    ("Q", "Extra-Territorial Organizations and Bodies"),
]
    # =====================================================
    # 🔷 BASIC INFO
    # =====================================================
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)


    active = models.BooleanField(default=True)

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

    industry = models.CharField( max_length=5, choices=INDUSTRY_SECTORS)

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

    physical_resources = models.ManyToManyField(
    'courses.PhysicalResource',
    blank=True,
    related_name='courses'
)

    # =====================================================
    # 🔷 DURATION & HOURS
    # =====================================================
    duration_months = models.PositiveIntegerField(default=0)

    theory_hours = models.FloatField(default=0)
    practical_hours = models.FloatField(default=0)
    assignment_hours = models.FloatField(default=0)

    ojt_months = models.FloatField(default=0)  # On Job Training

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

    # =====================================================
    # 🔷 PEDAGOGY
    # =====================================================
    prerequisite = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)

    # =====================================================
    # 🔷 SYSTEM
    # =====================================================
    STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')

    ncs = models.ForeignKey('courses.NCS', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    resources = models.ManyToManyField('courses.LearningResource', blank=True, related_name='courses_linked')
    # =====================================================
    # 🔥 CALCULATED TOTAL
    # =====================================================
    @property
    def total_hours(self):
        return (
            (self.theory_hours or 0) +
            (self.practical_hours or 0) +
            (self.assignment_hours or 0)
        )

    def clean(self):
        if self.is_free:
            self.course_fee = 0

    def __str__(self):
        return f"{self.code} - {self.title}"
