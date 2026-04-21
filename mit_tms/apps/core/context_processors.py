from .menu import (
    ADMIN_MENU,
    STAFF_MENU,
    TEACHER_MENU,
    STUDENT_MENU,
    PARENT_MENU,
    ALUMNI_MENU,
    GUEST_MENU,
)


def user_roles(request):
    user = request.user

    return {
        'is_admin': user.is_authenticated and user.is_superuser,
        'is_teacher': user.is_authenticated and hasattr(user, 'teacher'),
        'is_student': user.is_authenticated and hasattr(user, 'student'),
        'is_staff_user': user.is_authenticated and hasattr(user, 'staff'),
        'is_parent': user.is_authenticated and hasattr(user, 'parent'),
        'is_alumni': user.is_authenticated and hasattr(user, 'alumni'),
        'is_guest': user.is_authenticated and hasattr(user, 'guest'),
    }


def remove_duplicates(menu):
    seen = set()
    new_menu = []

    for section in menu:
        items = []
        for item in section["items"]:
            key = item["url"]

            if key not in seen:
                seen.add(key)
                items.append(item)

        if items:
            new_menu.append({
                "section": section["section"],
                "items": items
            })

    return new_menu


# def sidebar_menu(request):
#     user = request.user
#
#     if user.is_authenticated and user.is_superuser:
#         menu = remove_duplicates(ADMIN_MENU)   # ✅ APPLY HERE
#     else:
#         menu = []
#
#     return {
#         "admin_menu": menu,
#         "notification_count": 5,
#         "risk_count": 3,
#     }

def sidebar_menu(request):
    user = request.user

    # 🔒 Not logged in → guest menu
    if not user.is_authenticated:
        return {
            "sidebar_items": remove_duplicates(GUEST_MENU),
            "user_role": "GUEST",
        }

    # 🎯 Role priority (top → bottom)
    if user.is_superuser:
        role = "ADMIN"
        menu = ADMIN_MENU

    elif hasattr(user, "staff"):
        role = "STAFF"
        menu = STAFF_MENU

    elif hasattr(user, "teacher"):
        role = "TEACHER"
        menu = TEACHER_MENU

    elif hasattr(user, "student"):
        role = "STUDENT"
        menu = STUDENT_MENU

    elif hasattr(user, "parent"):
        role = "PARENT"
        menu = PARENT_MENU

    elif hasattr(user, "alumni"):
        role = "ALUMNI"
        menu = ALUMNI_MENU

    else:
        role = "GUEST"
        menu = GUEST_MENU

    return {
        "sidebar_items": remove_duplicates(menu),
        "user_role": role,  # useful in templates
    }
