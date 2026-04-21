from .models import LessonPlan, LessonActivity
from apps.courses.models import Task

def generate_lesson_plan(task, instructor=None):
    lesson, created = LessonPlan.objects.get_or_create(
        task=task,
        instructor=instructor,
        defaults={
            "title": f"Lesson: {task.title}",
            "subject": task.module.course.title,
            "level": task.module.course.level,
            "duration_minutes": int(task.duration_hours * 60),
            "competency": task.description,
            "materials": task.module.teaching_methods or "",
            "status": "generated"
        }
    )

    if not created:
        # 🔁 Regenerate (clear old activities)
        lesson.activities.all().delete()
        lesson.status = "updated"
        lesson.save()

    for i, activity in enumerate(task.activities.all()):
        LessonActivity.objects.create(
            lesson=lesson,
            activity_type=map_activity_type(activity.type),
            description=activity.description,
            duration_minutes=activity.duration_minutes,
            order=i
        )

    return lesson


def map_activity_type(activity_type):
    mapping = {
        "EXERCISE": "guided",
        "ASSIGNMENT": "independent",
        "MCQ": "assessment",
        "PRACTICAL": "presentation",
        "DISCUSSION": "intro",
    }
    return mapping.get(activity_type, "guided")
