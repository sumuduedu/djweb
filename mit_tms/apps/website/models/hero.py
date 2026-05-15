from django.db import models

from .section import Section


class HeroSection(models.Model):

    section = models.OneToOneField(
        Section,
        on_delete=models.CASCADE,
        related_name="hero"
    )

    badge = models.CharField(max_length=255)

    title = models.CharField(max_length=255)

    title_highlight = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField()

    button_text = models.CharField(max_length=100)

    button_link = models.CharField(max_length=255)

    secondary_button_text = models.CharField(
        max_length=100,
        blank=True
    )

    secondary_button_link = models.CharField(
        max_length=255,
        blank=True
    )

    background_image = models.ImageField(
        upload_to="hero/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
