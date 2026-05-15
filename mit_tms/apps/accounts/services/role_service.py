from django.db import transaction

from django.contrib.auth.models import (
    Group
)

from ..models import (
    Profile,
    Student,
    Teacher,
    Staff,
    Parent,
    Alumni
)


ROLE_GROUP_MAP = {
    Profile.ROLE_ADMIN: 'Admin',
    Profile.ROLE_STAFF: 'Staff',
    Profile.ROLE_TEACHER: 'Teacher',
    Profile.ROLE_STUDENT: 'Student',
    Profile.ROLE_PARENT: 'Parent',
    Profile.ROLE_ALUMNI: 'Alumni',
    Profile.ROLE_GUEST: 'Guest',
}


# =========================================================
# ASSIGN ROLE
# =========================================================

def assign_role(
    user,
    role
):

    if role not in dict(
        Profile.ROLE_CHOICES
    ):

        raise ValueError(
            'Invalid role'
        )

    profile = user.profile

    profile.role = role

    profile.save()


# =========================================================
# HANDLE ROLE CHANGE
# =========================================================

@transaction.atomic
def handle_role_change(
    profile
):

    user = profile.user

    if user.is_superuser:
        return

    full_name = (
        user.get_full_name()
        or user.username
    )

    deactivate_all_roles(user)

    if profile.role == (
        Profile.ROLE_STUDENT
    ):

        student, created = (
            Student.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': full_name,
                    'student_id': (
                        f'STU-{user.id}'
                    ),
                    'is_active': True
                }
            )
        )

        if not created:

            student.is_active = True
            student.full_name = full_name
            student.save()

    elif profile.role == (
        Profile.ROLE_TEACHER
    ):

        teacher, created = (
            Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': full_name,
                    'employee_id': (
                        f'TEC-{user.id}'
                    ),
                    'is_active': True
                }
            )
        )

        if not created:

            teacher.is_active = True
            teacher.full_name = full_name
            teacher.save()

    elif profile.role == (
        Profile.ROLE_STAFF
    ):

        staff, created = (
            Staff.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': full_name,
                    'employee_id': (
                        f'STF-{user.id}'
                    ),
                    'is_active': True
                }
            )
        )

        if not created:

            staff.is_active = True
            staff.full_name = full_name
            staff.save()

    elif profile.role == (
        Profile.ROLE_PARENT
    ):

        parent, created = (
            Parent.objects.get_or_create(
                user=user,
                defaults={
                    'is_active': True
                }
            )
        )

        if not created:

            parent.is_active = True
            parent.save()

    elif profile.role == (
        Profile.ROLE_ALUMNI
    ):

        alumni, created = (
            Alumni.objects.get_or_create(
                user=user,
                defaults={
                    'is_active': True
                }
            )
        )

        if not created:

            alumni.is_active = True
            alumni.save()

    sync_groups(
        user=user,
        role=profile.role
    )


# =========================================================
# DEACTIVATE ALL ROLES
# =========================================================

def deactivate_all_roles(
    user
):

    Student.objects.filter(
        user=user
    ).update(is_active=False)

    Teacher.objects.filter(
        user=user
    ).update(is_active=False)

    Staff.objects.filter(
        user=user
    ).update(is_active=False)

    Parent.objects.filter(
        user=user
    ).update(is_active=False)

    Alumni.objects.filter(
        user=user
    ).update(is_active=False)


# =========================================================
# GROUP SYNCHRONIZATION
# =========================================================

def sync_groups(
    user,
    role
):

    user.groups.clear()

    group_name = ROLE_GROUP_MAP.get(
        role
    )

    if not group_name:
        return

    group, _ = (
        Group.objects.get_or_create(
            name=group_name
        )
    )

    user.groups.add(group)


# =========================================================
# SYNC FULL NAMES
# =========================================================

def sync_full_names(
    user
):

    full_name = (
        user.get_full_name()
        or user.username
    )

    Student.objects.filter(
        user=user
    ).update(
        full_name=full_name
    )

    Teacher.objects.filter(
        user=user
    ).update(
        full_name=full_name
    )

    Staff.objects.filter(
        user=user
    ).update(
        full_name=full_name
    )
