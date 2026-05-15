from django.db import models

from .section import Section


class Statistic(models.Model):

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="statistics"
    )

    value = models.CharField(max_length=100)

    label = models.CharField(max_length=255)

    color = models.CharField(
        max_length=100,
        default="text-blue-600"
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label
