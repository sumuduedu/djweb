# core/context_processors.py
def user_roles(request):
    user = request.user

    return {
        'is_admin': user.is_authenticated and user.is_superuser,
        'is_teacher': user.is_authenticated and hasattr(user, 'teacher'),
        'is_student': user.is_authenticated and hasattr(user, 'student'),
    }
