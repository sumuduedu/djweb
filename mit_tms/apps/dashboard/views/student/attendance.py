from apps.attendance.models import (
    Attendance
)

from ..base import (
    BaseView
)


# =========================================================
# STUDENT ATTENDANCE VIEW
# =========================================================

class StudentAttendanceView(BaseView):

    template_name = (
        "student/attendance/list.html"
    )

    allowed_roles = ['STUDENT']

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        student = (
            self.request.user.student
        )

        attendance_records = (
            Attendance.objects
            .select_related(
                'batch',
                'session'
            )
            .filter(
                student=student
            )
            .order_by(
                '-date'
            )
        )

        total_records = (
            attendance_records.count()
        )

        present_count = (
            attendance_records.filter(
                status='PRESENT'
            ).count()
        )

        absent_count = (
            attendance_records.filter(
                status='ABSENT'
            ).count()
        )

        late_count = (
            attendance_records.filter(
                status='LATE'
            ).count()
        )

        attendance_percentage = 0

        if total_records > 0:

            attendance_percentage = round(

                (
                    present_count /
                    total_records
                ) * 100,

                2
            )

        context.update({

            'attendance_records':
                attendance_records,

            'total_records':
                total_records,

            'present_count':
                present_count,

            'absent_count':
                absent_count,

            'late_count':
                late_count,

            'attendance_percentage':
                attendance_percentage,
        })

        return context
