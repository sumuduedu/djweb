from django.utils.text import slugify
from .base import *
from .module import *

class Task(BaseModel):

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    code = models.CharField(max_length=20)

    title = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        blank=True,
        help_text="Auto-generated from title"
    )

    description = models.TextField(blank=True)

    duration_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_mandatory = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'code']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)

            # ensure uniqueness inside module
            slug = base_slug
            counter = 1

            while Task.objects.filter(module=self.module, slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.title}"
