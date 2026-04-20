from django.db import models

from django.db import models


class LessonPlan(models.Model):

    # 🔗 Link only to Task (clean design)
    task = models.ForeignKey(
        "courses.Task",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lesson_plans"
    )

    # 👨‍🏫 Instructor (🔥 REQUIRED FIX)
    instructor = models.ForeignKey(
        "accounts.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons"
    )

    # 🧾 Basic Info
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    date = models.DateField(null=True, blank=True)

    # 🎯 Teaching Info
    competency = models.TextField(blank=True)
    competency_level = models.CharField(
        max_length=50,
        choices=[
            ('basic', 'Basic'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='basic'
    )

    materials = models.TextField(blank=True)

    # 🕒 Tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class LearningOutcome(models.Model):
    lesson = models.ForeignKey(
        LessonPlan,
        on_delete=models.CASCADE,
        related_name='outcomes'
    )
    description = models.TextField()

    def __str__(self):
        return f"Outcome - {self.lesson.title}"

class LessonActivity(models.Model):

    ACTIVITY_TYPES = [
        ('intro', 'Introduction'),
        ('presentation', 'Presentation'),
        ('guided', 'Guided Practice'),
        ('independent', 'Independent Practice'),
        ('assessment', 'Assessment'),
        ('closure', 'Closure'),
    ]

    lesson = models.ForeignKey(
        LessonPlan,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField()
    duration_minutes = models.IntegerField()

    order = models.PositiveIntegerField(default=0)  # 🔥 better than IntegerField

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.lesson.title}"

# models.py
from django.conf import settings
class LessonSession(models.Model):
    lesson = models.ForeignKey(
        "lessonplan.LessonPlan",
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    batch = models.ForeignKey(
        "batch.Batch",
        on_delete=models.CASCADE
    )

    instructor = models.ForeignKey(
        "accounts.Teacher",   # 🔥 FIXED (IMPORTANT)
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.lesson.title} - {self.date}"

class Attendance(models.Model):
    session = models.ForeignKey(
        LessonSession,
        on_delete=models.CASCADE,
        related_name="attendance"
    )

    student = models.ForeignKey(
        "accounts.Student",
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('late', 'Late'),
        ]
    )

    check_in_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ['session', 'student']

    def __str__(self):
        return f"{self.student} - {self.status}"

class LessonPerformance(models.Model):
    session = models.ForeignKey(
        LessonSession,
        on_delete=models.CASCADE,
        related_name="performances"
    )

    student = models.ForeignKey(
        "accounts.Student",
        on_delete=models.CASCADE
    )

    understanding_level = models.IntegerField(
        help_text="1 (low) - 5 (high)"
    )

    participation_score = models.IntegerField(default=0)
    task_completion = models.BooleanField(default=False)

    score = models.FloatField(null=True, blank=True)

    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ['session', 'student']

    def __str__(self):
        return f"{self.student} - {self.session}"
