from django.db import models

from .section import Section


class Testimonial(models.Model):

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="testimonials"
    )

    name = models.CharField(max_length=100)

    role = models.CharField(max_length=100)

    message = models.TextField()

    rating = models.IntegerField(default=5)

    image = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name
