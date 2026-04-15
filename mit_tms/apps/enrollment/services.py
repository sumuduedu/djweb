from .models import Enrollment
from django.apps import apps


def enroll_student(user, batch_id):
    """
    Enroll logged-in student into a batch
    """
    if not hasattr(user, "student"):
        return None

    student = user.student

    Batch = apps.get_model("batch", "Batch")
    batch = Batch.objects.get(id=batch_id)

    enrollment, created = Enrollment.objects.get_or_create(
        student=student,
        batch=batch
    )

    return enrollment


def get_student_enrollments(user):
    if hasattr(user, "student"):
        return user.student.enrollments.select_related("batch__course").all()
    return []
