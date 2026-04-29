from math import floor

from .models import LessonPlan, LessonActivity
from apps.courses.models import Task


# =========================================
# 🎯 BASIC GENERATOR (RULE-BASED)
# =========================================
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

    # 🔁 regenerate
    if not created:
        lesson.activities.all().delete()
        lesson.status = "updated"
        lesson.save()

    # 🧠 simple pedagogical order
    FLOW_ORDER = {
        "MCQ": 1,
        "DISCUSSION": 2,
        "EXERCISE": 3,
        "PRACTICAL": 4,
        "ASSIGNMENT": 5,
    }

    activities = sorted(
        task.activities.all(),
        key=lambda x: FLOW_ORDER.get(x.type, 99)
    )

    order = 1

    for activity in activities:

        method = map_method(activity.type)
        trainer_time, trainee_time = split_time(activity.type, activity.duration_minutes or 30)
        trainer_flag, trainee_flag = map_role(activity.type)

        LessonActivity.objects.create(
            lesson=lesson,
            title=activity.title,
            description=activity.description or "",

            method=method,

            trainer_activity=trainer_flag,
            trainee_activity=trainee_flag,

            trainer_time=trainer_time,
            trainee_time=trainee_time,

            order=order
        )

        order += 1

    return lesson


# =========================================
# 🧠 SMART GENERATOR (BLOOM + TIME BASED)
# =========================================
def generate_smart_lesson_plan(task, instructor=None, session_hours=2):

    total_duration = session_hours * 60

    lesson, created = LessonPlan.objects.get_or_create(
        task=task,
        instructor=instructor,
        defaults={
            "title": f"Smart Lesson: {task.title}",
            "subject": task.module.course.title,
            "level": task.module.course.level,
            "duration_minutes": total_duration,
            "competency": task.description,
            "materials": task.module.teaching_methods or "",
            "status": "generated"
        }
    )

    if not created:
        lesson.activities.all().delete()
        lesson.status = "updated"
        lesson.save()

    # =========================================
    # 🧠 BLOOM FLOW
    # =========================================
    BLOOM_FLOW = [
        "remember",
        "understand",
        "apply",
        "analyze",
        "evaluate",
        "create"
    ]

    grouped = {level: [] for level in BLOOM_FLOW}

    for activity in task.activities.all():
        if activity.bloom_level:
            grouped[activity.bloom_level].append(activity)
        else:
            grouped["understand"].append(activity)

    # =========================================
    # ⏱ TIME DISTRIBUTION
    # =========================================
    BLOOM_TIME_RATIO = {
        "remember": 0.1,
        "understand": 0.2,
        "apply": 0.3,
        "analyze": 0.15,
        "evaluate": 0.15,
        "create": 0.1,
    }

    order = 1

    for level in BLOOM_FLOW:

        activities = grouped[level]
        if not activities:
            continue

        level_time = int(total_duration * BLOOM_TIME_RATIO[level])
        time_per_activity = max(10, floor(level_time / len(activities)))

        for activity in activities:

            method = map_method(activity.type)
            trainer_time, trainee_time = split_time(activity.type, time_per_activity)
            trainer_flag, trainee_flag = map_role(activity.type)

            LessonActivity.objects.create(
                lesson=lesson,
                title=f"[{level.upper()}] {activity.title}",
                description=activity.description or "",

                method=method,

                trainer_activity=trainer_flag,
                trainee_activity=trainee_flag,

                trainer_time=trainer_time,
                trainee_time=trainee_time,

                order=order
            )

            order += 1

    return lesson


# =========================================
# 🧠 METHOD MAPPING
# =========================================
def map_method(activity_type):
    mapping = {
        "EXERCISE": "PRACTICAL",
        "ASSIGNMENT": "GROUP",
        "MCQ": "LECTURE",
        "PRACTICAL": "PRACTICAL",
        "DISCUSSION": "DISCUSSION",
    }
    return mapping.get(activity_type, "LECTURE")


# =========================================
# ⏱ TIME SPLIT
# =========================================
def split_time(activity_type, total):

    if total <= 0:
        total = 30

    if activity_type == "PRACTICAL":
        return int(total * 0.2), int(total * 0.8)

    elif activity_type == "MCQ":
        return int(total * 0.8), int(total * 0.2)

    elif activity_type == "DISCUSSION":
        return int(total * 0.5), int(total * 0.5)

    elif activity_type == "ASSIGNMENT":
        return int(total * 0.3), int(total * 0.7)

    else:  # EXERCISE
        return int(total * 0.6), int(total * 0.4)


# =========================================
# 👥 ROLE LOGIC
# =========================================
def map_role(activity_type):

    if activity_type == "PRACTICAL":
        return False, True

    elif activity_type == "MCQ":
        return True, False

    elif activity_type == "ASSIGNMENT":
        return False, True

    elif activity_type == "DISCUSSION":
        return True, True

    else:
        return True, True
