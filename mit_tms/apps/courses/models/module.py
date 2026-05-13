from django.db import models
from django.utils.text import slugify
from .base import BaseModel


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

    slug = models.SlugField(max_length=255, blank=True)

    code = models.CharField(max_length=20,null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    module_type = models.CharField(
        max_length=20,
        choices=MODULE_TYPE_CHOICES,
        default='CORE'
    )

    duration_months = models.PositiveIntegerField(default=0)

    theory_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    practical_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    learning_outcomes = models.TextField(blank=True)

    theory_content = models.TextField(blank=True)
    practical_content = models.TextField(blank=True)

    teaching_methods = models.TextField(blank=True)
    assessment_methods = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'code']
        unique_together = [
            ['course', 'code'],
            ['course', 'slug'],
        ]
        indexes = [
            models.Index(fields=['course', 'order']),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if (self.theory_hours or 0) == 0 and (self.practical_hours or 0) == 0:
            raise ValidationError("Module must have at least theory or practical hours.")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)

            slug = base_slug
            counter = 1

            while Module.objects.filter(
                course=self.course,
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.title}"
