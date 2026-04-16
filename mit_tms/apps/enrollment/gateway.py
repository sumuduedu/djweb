try:
    from apps.enrollment.services import get_student_enrollments
except ImportError:
    def get_student_enrollments(user):
        return []
