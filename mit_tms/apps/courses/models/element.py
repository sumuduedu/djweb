from django.db import models
from .base import BaseModel
from .unit import Unit


class Element(BaseModel):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="elements"
    )

    code = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=255)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['unit', 'title']

    def __str__(self):
        return self.title
