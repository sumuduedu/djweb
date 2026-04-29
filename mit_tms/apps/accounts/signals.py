from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from allauth.account.signals import user_signed_up

from .models import Profile, Student, Teacher, Staff, Parent
from django.contrib.auth.models import Group

ROLE_GROUP_MAP = {
    'ADMIN': 'Admin',
    'STAFF': 'Staff',
    'TEACHER': 'Teacher',
    'STUDENT': 'Student',
    'PARENT': 'Parent',
    'ALUMNI': 'Alumni',
    'GUEST': 'Guest',
}

# ================================
# 🔷 CREATE PROFILE (DEFAULT = GUEST)
# ================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            role='GUEST'   # 🔥 DEFAULT ROLE
        )


# ================================
# 🔷 GOOGLE / SOCIAL LOGIN
# ================================
@receiver(user_signed_up)
def assign_role_social_login(request, user, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=user)

    # 🔥 ensure role exists
    if not profile.role:
        profile.role = 'GUEST'
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
# 🔷 CREATE / REMOVE ROLE MODELS
# ================================
@receiver(post_save, sender=Profile)
def create_role_models(sender, instance, created, **kwargs):

    user = instance.user

    # 🔥 skip superuser
    if user.is_superuser:
        return

    role_changed = (
        created or
        getattr(instance, "_previous_role", None) != instance.role
    )

    if not role_changed:
        return

    full_name = user.get_full_name() or user.username

    # ============================
    # 🎓 STUDENT
    # ============================
    if instance.role == 'STUDENT':
        Student.objects.get_or_create(
            user=user,
            defaults={"full_name": full_name}
        )

        Teacher.objects.filter(user=user).delete()
        Staff.objects.filter(user=user).delete()
        Parent.objects.filter(user=user).delete()

    # ============================
    # 👨‍🏫 TEACHER
    # ============================
    elif instance.role == 'TEACHER':
        Teacher.objects.get_or_create(
            user=user,
            defaults={"full_name": full_name}
        )

        Student.objects.filter(user=user).delete()
        Staff.objects.filter(user=user).delete()
        Parent.objects.filter(user=user).delete()

    # ============================
    # 🧑‍💼 STAFF
    # ============================
    elif instance.role == 'STAFF':
        Staff.objects.get_or_create(
            user=user,
            defaults={"full_name": full_name}
        )

        Student.objects.filter(user=user).delete()
        Teacher.objects.filter(user=user).delete()
        Parent.objects.filter(user=user).delete()

    # ============================
    # 👨‍👩‍👧 PARENT
    # ============================
    elif instance.role == 'PARENT':
        Parent.objects.get_or_create(
            user=user
        )

        Student.objects.filter(user=user).delete()
        Teacher.objects.filter(user=user).delete()
        Staff.objects.filter(user=user).delete()

    # ============================
    # 👤 GUEST / 🎓 ALUMNI
    # ============================
    elif instance.role in ['GUEST', 'ALUMNI']:
        Student.objects.filter(user=user).delete()
        Teacher.objects.filter(user=user).delete()
        Staff.objects.filter(user=user).delete()
        Parent.objects.filter(user=user).delete()


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

    staff = getattr(instance, "staff", None)
    if staff:
        staff.full_name = full_name
        staff.save()
