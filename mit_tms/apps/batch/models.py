from django.db import models
from datetime import timedelta

from apps.courses.models import Course, Module


# =========================================================
# 🔷 ACADEMIC YEAR
# =========================================================

class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


# =========================================================
# 🔷 BATCH
# =========================================================
from django.db import models
from apps.courses.models import Course
from apps.accounts.models import Teacher



class Batch(models.Model):

    name = models.CharField(max_length=255)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="batches"
    )

    # ✅ ADD THIS
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="batches"
    )

    start_date = models.DateField()

    # ✅ ADD THIS
    end_date = models.DateField(null=True, blank=True)

    # ✅ ADD THIS
    capacity = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

