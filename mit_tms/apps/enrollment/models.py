from django.db import models
from django.contrib.auth.models import User
from apps.courses.models import Course

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)

    role_type = models.CharField(max_length=10, choices=ROLE_TYPE)

    full_name = models.CharField(max_length=255)
    email = models.EmailField()

    phone = models.CharField(max_length=20)
    address = models.TextField()
    qualification = models.CharField(max_length=255, blank=True, null=True)

    # 👨‍👩‍👧 Parent fields
    student_name = models.CharField(max_length=255, blank=True, null=True)
    student_age = models.IntegerField(blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)

    # 📌 Status
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        db_index=True
    )

    rejection_reason = models.TextField(blank=True, null=True)

    # 📝 Optional notes
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']

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

    def __str__(self):
        return f"{self.student.full_name} → {self.batch}"
