from .base import BaseModel
from django.db import models
from .module import Module

class Task(BaseModel):

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='tasks')


    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    duration_hours = models.PositiveIntegerField(default=0)
    is_mandatory = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)
    ncs_element = models.ForeignKey(
    'courses.Element',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='tasks'
)

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'title']

    def __str__(self):
        return self.title
