from django.db import models
from .base import BaseModel
from .course import *

class Unit(BaseModel):

    ncs = models.ForeignKey(
        'NCS',
        on_delete=models.CASCADE,
        related_name="nsc_unit"
    )
    course = models.ForeignKey(Course, null=True, blank=True,on_delete=models.CASCADE,
        related_name="course_unit")

    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    level = models.IntegerField(null=True, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['ncs', 'code']

    def __str__(self):
        return f"{self.title} ({self.code})"
