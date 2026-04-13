from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from allauth.account.signals import user_signed_up

from .models import Profile, Student, Teacher


# ================================
# 🔷 CREATE PROFILE + DEFAULT ROLE
# ================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, _ = Profile.objects.get_or_create(user=instance)

        # 🔥 Ensure default role
        if not profile.role:
            profile.role = 'STUDENT'
            profile.save()


# ================================
# 🔷 GOOGLE / SOCIAL LOGIN ROLE ASSIGN
# ================================
@receiver(user_signed_up)
def assign_role_social_login(request, user, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=user)

    # 🔥 Default role for social users
    if not profile.role:
        profile.role = 'STUDENT'
        profile.save()


# ================================
# 🔷 STORE OLD ROLE (FOR CHANGE DETECTION)
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
# 🔷 CREATE STUDENT / TEACHER BASED ON ROLE
# ================================
@receiver(post_save, sender=Profile)
def create_role_model(sender, instance, created, **kwargs):

    user = instance.user

    # 🔥 Skip superuser
    if user.is_superuser:
        return

    # 🔥 Check if role changed
    role_changed = (
        created or
        getattr(instance, "_previous_role", None) != instance.role
    )

    if not role_changed:
        return

    # 🔥 STUDENT ROLE
    if instance.role == 'STUDENT':
        Student.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.get_full_name() or user.username
            }
        )
        Teacher.objects.filter(user=user).delete()

    # 🔥 TEACHER ROLE
    elif instance.role == 'TEACHER':
        Teacher.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.get_full_name() or user.username
            }
        )
        Student.objects.filter(user=user).delete()


# ================================
# 🔷 SYNC NAME WHEN USER UPDATED
# ================================
@receiver(post_save, sender=User)
def update_names(sender, instance, **kwargs):

    full_name = instance.get_full_name() or instance.username

    student = getattr(instance, "student", None)
    if student:
        student.full_name = full_name
        student.save()

    teacher = getattr(instance, "teacher", None)
    if teacher:
        teacher.full_name = full_name
        teacher.save()
