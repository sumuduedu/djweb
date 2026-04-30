from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from core.models import PermissionRule

DEFAULT_ENTITIES = ["module", "course"]
DEFAULT_ACTIONS = ["create", "read", "update", "delete"]

def create_default_permissions(sender, instance, created, **kwargs):
    if created:
        for entity in DEFAULT_ENTITIES:
            for action in DEFAULT_ACTIONS:
                PermissionRule.objects.create(
                    group=instance,
                    entity=entity,
                    action=action,
                    allowed=False
                )

post_save.connect(create_default_permissions, sender=Group)
