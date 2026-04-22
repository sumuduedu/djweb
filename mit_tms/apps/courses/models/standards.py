from django.db import models
from .base import BaseModel


class TaskStandard(BaseModel):
    task = models.ForeignKey(
        'courses.Task',
        on_delete=models.CASCADE,
        related_name='standards'
    )

    description = models.TextField()

    order = models.PositiveIntegerField(default=0)

    is_mandatory = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        unique_together = ['task', 'description']

    def __str__(self):
        return self.description[:50]
