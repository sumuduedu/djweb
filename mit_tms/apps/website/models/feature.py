from django.db import models

from .section import Section


class Feature(models.Model):

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="features"
    )

    icon = models.CharField(max_length=50)

    title = models.CharField(max_length=255)

    description = models.TextField()

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
