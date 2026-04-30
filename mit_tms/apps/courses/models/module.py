from .base import BaseModel
from django.db import models

class Module(BaseModel):

    MODULE_TYPE_CHOICES = [
        ('CORE', 'Core Module'),
        ('ELECTIVE', 'Elective Module'),
        ('BASIC', 'Basic Module'),
    ]

    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='modules'
    )


    # 🔷 BASIC INFO
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    module_type = models.CharField(max_length=20, choices=MODULE_TYPE_CHOICES)

    # 🔷 DURATION
    duration_months = models.PositiveIntegerField(default=0)
    total_hours = models.FloatField(default=0)
    theory_hours = models.FloatField(default=0)
    practical_hours = models.FloatField(default=0)

    # 🔷 LEARNING OUTCOMES
    learning_outcomes = models.TextField(
        help_text="Write outcomes as bullet points"
    )

    # 🔷 LEARNING CONTENT
    theory_content = models.TextField(blank=True)
    practical_content = models.TextField(blank=True)

    # 🔷 TEACHING METHODS
    teaching_methods = models.TextField(blank=True)

    # 🔷 ASSESSMENT METHODS
    assessment_methods = models.TextField(blank=True)

    # 🔷 ORDERING
    order = models.PositiveIntegerField(default=0)





    class Meta:
        ordering = ['order', 'code']
        unique_together = ['course', 'code']

    def __str__(self):
        return f"{self.code} - {self.title}"
