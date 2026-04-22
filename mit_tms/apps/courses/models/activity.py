from .resource import LearningResource

from django.db import models
from apps.courses.models import Task


class Activity(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    duration_minutes = models.PositiveIntegerField(default=0)

    ACTIVITY_TYPE = [
        ('EXERCISE', 'Exercise'),
        ('ASSIGNMENT', 'Assignment'),
        ('MCQ', 'MCQ'),
        ('PRACTICAL', 'Practical'),
        ('DISCUSSION', 'Discussion'),
    ]

    type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE,
        default='EXERCISE'
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.task.title})"
