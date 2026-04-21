from django.db import models


# ================================
# 📘 LESSON PLAN
# ================================
class LessonPlan(models.Model):

    task = models.ForeignKey(
        "courses.Task",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lesson_plans"
    )

    instructor = models.ForeignKey(
        "accounts.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons"
    )

    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    date = models.DateField(null=True, blank=True)

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

    # 🔥 3 DOMAINS
    cognitive = models.BooleanField(default=False)
    psychomotor = models.BooleanField(default=False)
    affective = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('generated', 'Generated'),
            ('updated', 'Updated'),
        ],
        default='draft'
    )

    materials = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def subject_name(self):
        return self.task.module.title if self.task else ""

    # 🔥 TOTAL TIME CALCULATION
    def total_activity_time(self):
        return sum(a.total_time for a in self.activities.all())

    # 🔥 VALIDATION
    def is_time_valid(self):
        return self.total_activity_time() == self.duration_minutes


# ================================
# 🎯 LEARNING OUTCOME
# ================================
class LearningOutcome(models.Model):
    lesson = models.ForeignKey(
        LessonPlan,
        on_delete=models.CASCADE,
        related_name='outcomes'
    )
    description = models.TextField()

    def __str__(self):
        return f"Outcome - {self.lesson.title}"


# ================================
# 🪜 LESSON ACTIVITY (NVQ STYLE)
# ================================
class LessonActivity(models.Model):

    lesson = models.ForeignKey(
        LessonPlan,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    # WHO DOES
    trainer_activity = models.BooleanField(default=False)
    trainee_activity = models.BooleanField(default=False)

    # METHOD + RESOURCES
    method = models.CharField(max_length=255, blank=True)
    resources = models.TextField(blank=True)

    # TIME
    trainer_time = models.PositiveIntegerField(default=0)
    trainee_time = models.PositiveIntegerField(default=0)
    total_time = models.PositiveIntegerField(default=0)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        self.total_time = self.trainer_time + self.trainee_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.lesson.title}"


# ================================
# 🏫 LESSON SESSION (DELIVERY)
# ================================
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
        "accounts.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )

    def __str__(self):
        return f"{self.lesson.title} ({self.batch}) - {self.date}"


# ================================
# 📋 ATTENDANCE
# ================================
class Attendance(models.Model):
    session = models.ForeignKey(
        "lessonplan.LessonSession",
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


# ================================
# 📊 PERFORMANCE
# ================================
class LessonPerformance(models.Model):
    session = models.ForeignKey(
        "lessonplan.LessonSession",   # 🔥 FIXED
        on_delete=models.CASCADE,
        related_name="performances"
    )

    student = models.ForeignKey(
        "accounts.Student",
        on_delete=models.CASCADE
    )

    understanding_level = models.IntegerField(help_text="1-5")

    participation_score = models.IntegerField(default=0)
    task_completion = models.BooleanField(default=False)

    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ['session', 'student']

    def __str__(self):
        return f"{self.student} - {self.session}"
