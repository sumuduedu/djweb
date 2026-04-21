from django.db import models
from django.contrib.auth.models import User
from apps.courses.models import Course

from django.db import models
from django.contrib.auth.models import User


class EnrollmentInquiry(models.Model):

    ROLE_TYPE = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
        ('PARENT', 'Parent'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    TIMELINE_STAGES = (
        ('SUBMITTED', 'Submitted'),
        ('REVIEW', 'Under Review'),
        ('INTERVIEW', 'Interview'),
        ('FINAL', 'Final Decision'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)

    role_type = models.CharField(max_length=10, choices=ROLE_TYPE)

    # 👤 Basic Info
    full_name = models.CharField(max_length=255)
    email = models.EmailField()

    phone = models.CharField(max_length=20)

    # 🏠 Address (use these instead of old one)
    current_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)

    # 📞 Extra contact
    home_phone = models.CharField(max_length=20, blank=True, null=True)

    # 🎓 Qualification
    qualification = models.CharField(max_length=255, blank=True, null=True)

    # 🪪 NIC
    nic_number = models.CharField(max_length=20, blank=True, null=True)
    nic_copy = models.ImageField(upload_to='nic/', blank=True, null=True)

    # 🔍 Verification
    is_nic_verified = models.BooleanField(default=False)
    is_contact_verified = models.BooleanField(default=False)

    # 👨‍👩‍👧 Parent Info
    parent_name = models.CharField(max_length=255, blank=True, null=True)
    parent_email = models.EmailField(blank=True, null=True)

    parent_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_parent_accounts"
    )

    student_name = models.CharField(max_length=255, blank=True, null=True)
    student_age = models.IntegerField(blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)

    # 📊 AI
    risk_score = models.FloatField(blank=True, null=True)
    is_flagged = models.BooleanField(default=False)

    # 📌 Status + Timeline
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        db_index=True
    )

    current_stage = models.CharField(
        max_length=20,
        choices=TIMELINE_STAGES,
        default='SUBMITTED'
    )

    rejection_reason = models.TextField(blank=True, null=True)

    # 📝 Notes
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_application')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.status})"

class Enrollment(models.Model):
    student = models.ForeignKey(
        "accounts.Student",
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    batch = models.ForeignKey(
        "batch.Batch",
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'batch'], name='unique_student_batch')
        ]

    def __str__(self):
        return f"{self.student.full_name} → {self.batch}"
    # apps/enrollment/models.py

    TIMELINE_STAGES = (
        ('SUBMITTED', 'Submitted'),
        ('REVIEW', 'Under Review'),
        ('INTERVIEW', 'Interview'),
        ('FINAL', 'Final Decision'),
    )

    current_stage = models.CharField(
        max_length=20,
        choices=TIMELINE_STAGES,
        default='SUBMITTED'
    )

class OLResult(models.Model):
    application = models.ForeignKey(
        'EnrollmentInquiry',
        on_delete=models.CASCADE,
        related_name='ol_results'
    )
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.subject} - {self.grade}"


class ALResult(models.Model):
    application = models.ForeignKey(
        'EnrollmentInquiry',
        on_delete=models.CASCADE,
        related_name='al_results'
    )
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.subject} - {self.grade}"
