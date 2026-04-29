from django.db import models
from .base import BaseModel


class Assessment(BaseModel):

    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name="assessments",
        null=True,
        blank=True
    )

    task = models.ForeignKey(
            'courses.Task',
            on_delete=models.CASCADE,
            related_name='course_assessments',  # ✅ FIX
            null=True,
            blank=True
        )

    title = models.CharField(max_length=255)

    ASSESSMENT_TYPE = [
        ('FORMATIVE', 'Formative'),
        ('SUMMATIVE', 'Summative'),
        ('PROJECT', 'Project'),
    ]

    type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE)

    max_marks = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)   # ✅ ADD THIS

    def __str__(self):
        return self.title

# courses/models/assessment.py

class TaskAssessment(BaseModel):
    task = models.ForeignKey(
        'courses.Task',
        on_delete=models.CASCADE,
        related_name='task_assessments'  # ✅ FIX
    )
    title = models.CharField(max_length=255)

    ASSESSMENT_TYPE = [
        ('FORMATIVE', 'Formative'),
        ('SUMMATIVE', 'Summative'),
    ]

    type = models.CharField(
        max_length=20,
        choices=ASSESSMENT_TYPE,
        default='FORMATIVE'
    )

    max_marks = models.PositiveIntegerField()

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        unique_together = ['task', 'title']

    def __str__(self):
        return self.title
