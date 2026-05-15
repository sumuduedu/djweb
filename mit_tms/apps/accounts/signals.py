from django.db.models.signals import (
    post_save,
    pre_save
)

from django.dispatch import receiver

from django.contrib.auth import (
    get_user_model
)

from allauth.account.signals import (
    user_signed_up
)

from .models import (
    Profile
)

from .services.role_service import (
    handle_role_change,
    sync_full_names
)


User = get_user_model()


# =========================================================
# CREATE PROFILE
# =========================================================

@receiver(post_save, sender=User)
def create_user_profile(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        Profile.objects.get_or_create(
            user=instance,
            defaults={
                'role': Profile.ROLE_GUEST
            }
        )


# =========================================================
# SOCIAL LOGIN PROFILE
# =========================================================

@receiver(user_signed_up)
def assign_role_social_login(
    request,
    user,
    **kwargs
):

    Profile.objects.get_or_create(
        user=user,
        defaults={
            'role': Profile.ROLE_GUEST
        }
    )


# =========================================================
# STORE OLD ROLE
# =========================================================

@receiver(pre_save, sender=Profile)
def store_previous_role(
    sender,
    instance,
    **kwargs
):

    if instance.pk:

        try:

            old_profile = (
                Profile.objects.get(
                    pk=instance.pk
                )
            )

            instance._previous_role = (
                old_profile.role
            )

        except Profile.DoesNotExist:

            instance._previous_role = None

    else:

        instance._previous_role = None


# =========================================================
# HANDLE ROLE CHANGE
# =========================================================

@receiver(post_save, sender=Profile)
def manage_role_models(
    sender,
    instance,
    created,
    **kwargs
):

    role_changed = (
        created
        or
        getattr(
            instance,
            '_previous_role',
            None
        ) != instance.role
    )

    if not role_changed:
        return

    handle_role_change(
        profile=instance
    )


# =========================================================
# SYNC FULL NAMES
# =========================================================

@receiver(post_save, sender=User)
def sync_user_full_names(
    sender,
    instance,
    **kwargs
):

    sync_full_names(
        user=instance
    )
