from django.db import models

# Create your models here.
# apps/accounts/models.py

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
