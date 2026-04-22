from django.db import models
from .base import BaseModel

class PhysicalResource(models.Model):

    RESOURCE_TYPE = [
        ('TOOL', 'Tool'),
        ('EQUIPMENT', 'Equipment'),
        ('MACHINE', 'Machinery'),
        ('FACILITY', 'Facility'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=RESOURCE_TYPE)

    def __str__(self):
        return self.name

class LearningResource(models.Model):

    RESOURCE_TYPE = [
        ('VIDEO', 'Video'),
        ('PDF', 'PDF'),
        ('LINK', 'External Link'),
        ('DOC', 'Document'),
        ('IMAGE', 'Image'),
    ]
    course = models.ForeignKey(
    'courses.Course',
    on_delete=models.CASCADE,
    related_name='learning_resources'
)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=RESOURCE_TYPE)

    file = models.FileField(upload_to='resources/', null=True, blank=True)
    url = models.URLField(blank=True)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
