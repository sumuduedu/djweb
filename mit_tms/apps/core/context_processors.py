# ================================
# 📦 IMPORTS
# ================================
from .menu import (
    ADMIN_MENU,
    STUDENT_MENU,
    TEACHER_MENU,
    STAFF_MENU,
    ALUMNI_MENU,
    PARENT_MENU,
)


# ================================
# 👤 USER ROLE FLAGS
# ================================
def user_roles(request):
    user = request.user

    return {
        "is_admin": user.is_authenticated and user.is_superuser,
        "is_teacher": user.is_authenticated and hasattr(user, "teacher"),
        "is_student": user.is_authenticated and hasattr(user, "student"),
        "is_staff_user": user.is_authenticated and hasattr(user, "staff"),
        "is_parent": user.is_authenticated and hasattr(user, "parent"),
        "is_alumni": user.is_authenticated and hasattr(user, "alumni"),
    }


# ================================
# 🔁 REMOVE DUPLICATE MENU ITEMS
# ================================
def remove_duplicates(menu):
    seen = set()
    new_menu = []

    for section in menu:
        items = []

        for item in section.get("items", []):
            key = item.get("url")

            if key and key not in seen:
                seen.add(key)
                items.append(item)

        if items:
            new_menu.append({
                "section": section.get("section"),
                "items": items
            })

    return new_menu


# ================================
# 📊 SIDEBAR MENU (MAIN ENGINE)
# ================================
def sidebar_menu(request):
    user = request.user

    # Default values
    menu = []
    notification_count = 0
    risk_count = 0

    # 🚫 Not logged in
    if not user.is_authenticated:
        return {
            "menu": [],
            "notification_count": 0,
            "risk_count": 0,
        }

    # ================================
    # 🎯 ROLE-BASED MENU SELECTION
    # ================================
    if user.is_superuser:
        menu = remove_duplicates(ADMIN_MENU)

    elif hasattr(user, "student"):
        menu = STUDENT_MENU
        # Example dynamic values (replace later with DB / ML)
        notification_count = 5
        risk_count = 3

    elif hasattr(user, "teacher"):
        menu = TEACHER_MENU

    elif hasattr(user, "staff"):
        menu = STAFF_MENU

    elif hasattr(user, "alumni"):
        menu = ALUMNI_MENU

    elif hasattr(user, "parent"):
        menu = PARENT_MENU

    # ================================
    # 📦 RETURN CONTEXT
    # ================================
    return {
        "menu": menu,
        "notification_count": notification_count,
        "risk_count": risk_count,
    }
