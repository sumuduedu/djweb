from .menu import ADMIN_MENU,STUDENT_MENU,GUEST_MENU


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

    print("USER:", user)
    print("AUTH:", user.is_authenticated)

    if user.is_authenticated:
        print("CHECKING ROLES...")

        if user.is_superuser:
            print("ADMIN")
            menu = remove_duplicates(ADMIN_MENU)

        elif hasattr(user, 'student'):
            print("STUDENT DETECTED")
            menu = remove_duplicates(STUDENT_MENU)

        else:
            print("GUEST")
            menu = remove_duplicates(GUEST_MENU)

    else:
        menu = []

    print("MENU:", menu)

    return {
        "sidebar_items": menu,
    }
