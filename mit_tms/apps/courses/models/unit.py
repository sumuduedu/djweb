from django.db import models
from .base import BaseModel
from .course import Course


class Unit(BaseModel):

    ncs = models.ForeignKey(
        'courses.NCS',
        on_delete=models.CASCADE,
        related_name="units"   # ✅ fixed name
    )

    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="units"   # ✅ consistent naming
    )

    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    level = models.IntegerField(null=True, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['ncs', 'code']  # ✅ correct

    def __str__(self):
        return f"{self.code} - {self.title}"
