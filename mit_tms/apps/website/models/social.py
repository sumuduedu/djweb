from django.db import models


class SocialLink(models.Model):

    PLATFORM_CHOICES = [

        ("FACEBOOK", "Facebook"),
        ("INSTAGRAM", "Instagram"),
        ("YOUTUBE", "YouTube"),
        ("LINKEDIN", "LinkedIn"),

    ]

    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES
    )

    icon = models.CharField(max_length=100)

    url = models.URLField()

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.platform
