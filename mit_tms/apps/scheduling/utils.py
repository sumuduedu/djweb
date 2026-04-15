from datetime import timedelta
from collections import defaultdict

from .models import Timetable


# =========================================================
# 🔷 TIMETABLE GENERATION (GRID BASED)
# =========================================================

def generate_timetable(batch):

    # 🔥 CLEAR OLD DATA
    batch.timetable.all().delete()

    modules = batch.course.modules.all().order_by('order')

    current_week = 1
    current_day = 1
    current_slot = 1

    max_slots_per_day = int(batch.hours_per_day)

    for module in modules:

        total_hours = (module.theory_hours or 0) + (module.practical_hours or 0)

        while total_hours > 0:

            Timetable.objects.create(
                batch=batch,
                module=module,
                week=current_week,
                day=current_day,
                row_slot=current_slot
            )

            total_hours -= 1
            current_slot += 1

            # 🔥 move to next day
            if current_slot > max_slots_per_day:
                current_slot = 1
                current_day += 1

            # 🔥 move to next week
            if current_day > batch.days_per_week:
                current_day = 1
                current_week += 1

    return True


# =========================================================
# 🔷 MONTHLY PLAN (WEEK-BASED SUMMARY)
# =========================================================

def get_monthly_plan(batch):

    monthly_plan = defaultdict(lambda: defaultdict(float))

    timetable = batch.timetable.all()

    for entry in timetable:

        # Group by week
        month = f"Week {entry.week}"

        monthly_plan[month][entry.module.title] += 1

    result = []

    for month, modules in monthly_plan.items():
        result.append({
            "month": month,
            "modules": dict(modules),
            "total": sum(modules.values())
        })

    return result
