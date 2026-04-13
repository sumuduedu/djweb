from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Student, Teacher


# ================================
# 🔷 CREATE PROFILE
# ================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


# ================================
# 🔷 STORE OLD ROLE
# ================================
@receiver(pre_save, sender=Profile)
def store_previous_role(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_role = Profile.objects.get(pk=instance.pk).role
        except Profile.DoesNotExist:
            instance._previous_role = None
    else:
        instance._previous_role = None


# ================================
# 🔷 CREATE STUDENT / TEACHER
# ================================
@receiver(post_save, sender=Profile)
def create_role_model(sender, instance, created, **kwargs):

    user = instance.user

    if user.is_superuser:
        return

    role_changed = (
        created or
        getattr(instance, "_previous_role", None) != instance.role
    )

    if not role_changed:
        return

    if instance.role == 'STUDENT':
        Student.objects.get_or_create(
            user=user,
            defaults={"full_name": user.get_full_name() or user.username}
        )
        Teacher.objects.filter(user=user).delete()

    elif instance.role == 'TEACHER':
        Teacher.objects.get_or_create(
            user=user,
            defaults={"full_name": user.get_full_name() or user.username}
        )
        Student.objects.filter(user=user).delete()


# ================================
# 🔷 SYNC NAME
# ================================
@receiver(post_save, sender=User)
def update_names(sender, instance, **kwargs):
    if hasattr(instance, "student"):
        instance.student.full_name = instance.get_full_name() or instance.username
        instance.student.save()

    if hasattr(instance, "teacher"):
        instance.teacher.full_name = instance.get_full_name() or instance.username
        instance.teacher.save()
