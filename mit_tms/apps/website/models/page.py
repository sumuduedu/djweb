from django.db import models


class Page(models.Model):

    PAGE_TYPES = [

        ("HOME", "Home"),
        ("ABOUT", "About"),
        ("BLOG", "Blog"),
        ("CONTACT", "Contact"),
        ("COURSES", "Courses"),

    ]

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    page_type = models.CharField(
        max_length=50,
        choices=PAGE_TYPES
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
