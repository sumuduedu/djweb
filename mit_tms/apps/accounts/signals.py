from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Student, Teacher


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        # Auto create based on role (default STUDENT)
        if profile.role == 'STUDENT':
            Student.objects.create(user=instance, full_name=instance.username)


@receiver(post_save, sender=Profile)
def create_role_model(sender, instance, created, **kwargs):

    if instance.role == 'STUDENT':
        Student.objects.get_or_create(
            user=instance.user,
            defaults={"full_name": instance.user.username}
        )

    elif instance.role == 'TEACHER':
        Teacher.objects.get_or_create(
            user=instance.user,
            defaults={"full_name": instance.user.username}
        )
