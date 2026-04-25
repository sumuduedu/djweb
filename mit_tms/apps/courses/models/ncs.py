
from django.db import models

# Create your models here.

class NCS(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    level = models.IntegerField()  # 1–4

    sector = models.CharField(max_length=255)
    version = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)  # ✅ IMPORTANT

    def __str__(self):
        return f"{self.code} - {self.name}"


class Package(models.Model):
    ncs = models.ForeignKey(
        'courses.NCS',
        on_delete=models.CASCADE,
        related_name='packages'
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
