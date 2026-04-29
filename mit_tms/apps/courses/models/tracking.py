from django.db import models
from .base import BaseModel
from django.utils.timezone import now

class StudentTask(BaseModel):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    task = models.ForeignKey('courses.Task', on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NOT_STARTED'
    )

    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    competency_achieved = models.BooleanField(default=False)

    started_at = models.DateTimeField(null=True, blank=True,default=now)
    completed_at = models.DateTimeField(null=True, blank=True,default=now)

    attempts = models.PositiveIntegerField(default=1)
