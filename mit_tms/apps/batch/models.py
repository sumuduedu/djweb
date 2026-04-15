from django.db import models
from datetime import timedelta

from apps.courses.models import Course, Module


# =========================================================
# 🔷 UTIL FUNCTION
# =========================================================

def calculate_end_date(batch):
    total_hours = batch.course.total_hours
    weekly_hours = batch.hours_per_day * batch.days_per_week

    if weekly_hours == 0:
        return batch.start_date

    total_weeks = total_hours / weekly_hours
    total_days = int(total_weeks * batch.days_per_week)

    return batch.start_date + timedelta(days=total_days)


# =========================================================
# 🔷 TIME SLOT
# =========================================================

class TimeSlot(models.Model):
    name = models.CharField(max_length=50, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    order = models.IntegerField()
    is_break = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']  # ✅ added (safe improvement)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


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

class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    start_date = models.DateField()

    hours_per_day = models.FloatField()
    days_per_week = models.IntegerField()

    max_students = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 AUTO CALCULATED END DATE
    @property
    def end_date(self):
        if not self.start_date:
            return None
        return calculate_end_date(self)

    def __str__(self):
        return f"{self.course.code} - {self.name}"


# =========================================================
# 🔷 TIMETABLE
# =========================================================

class Timetable(models.Model):
    batch = models.ForeignKey(
        'Batch',
        on_delete=models.CASCADE,
        related_name='timetable'
    )

    module = models.ForeignKey('courses.Module', on_delete=models.CASCADE)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    week = models.IntegerField()

    DAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]

    day = models.IntegerField(choices=DAY_CHOICES)
    row_slot = models.IntegerField()

    hours = models.FloatField(default=1)

    SESSION_TYPES = (
        ('THEORY', 'Theory'),
        ('PRACTICAL', 'Practical'),
    )

    session_type = models.CharField(
        max_length=10,
        choices=SESSION_TYPES,
        default='THEORY'
    )

    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch", "day", "row_slot"],
                name="unique_batch_day_slot"
            )
        ]

    def __str__(self):
        return f"{self.batch} - Day {self.day} Slot {self.row_slot}"


# =========================================================
# 🔷 SESSION
# =========================================================

class Session(models.Model):
    timetable = models.OneToOneField(
        Timetable,
        on_delete=models.CASCADE,
        related_name='session'
    )

    conducted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['timetable__date']

    def __str__(self):
        return f"Session - {self.timetable.date}"


# =========================================================
# 🔷 MODULE PLAN
# =========================================================

class ModulePlan(models.Model):
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, related_name='plans')
    module = models.ForeignKey('courses.Module', on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    theory_hours = models.FloatField(default=0)
    practical_hours = models.FloatField(default=0)

    def __str__(self):
        return f"{self.module.title} ({self.start_date} - {self.end_date})"

