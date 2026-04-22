# courses/models/criteria.py

from django.db import models
from .element import Element


class PerformanceCriteria(models.Model):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name="criteria"
    )
    description = models.TextField()

    def __str__(self):
        return self.description[:50]
