from django.db import models

# Create your models here.
from django.contrib.auth.models import Group
from django.db import models

class PermissionRule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    entity = models.CharField(max_length=50)   # "module", "course"
    action = models.CharField(max_length=20)   # create/read/update/delete
    allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = ("group", "entity", "action")
