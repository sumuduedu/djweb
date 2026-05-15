from django.db import models

from .page import Page


class Section(models.Model):

    SECTION_TYPES = [

        ("HERO", "Hero"),
        ("ABOUT", "About"),
        ("FEATURES", "Features"),
        ("STATS", "Statistics"),
        ("COURSES", "Courses"),
        ("TESTIMONIALS", "Testimonials"),
        ("CTA", "Call To Action"),

    ]

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="sections"
    )

    title = models.CharField(max_length=255)

    section_type = models.CharField(
        max_length=50,
        choices=SECTION_TYPES
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.page.title} - {self.title}"
