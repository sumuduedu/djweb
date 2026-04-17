from .base import BaseView


class TeacherDashboardView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teacher.html"

class TeacherCoursesView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        courses = [
            {"title": "Python Programming", "batches": 2},
            {"title": "Web Design", "batches": 1},
        ]

        context["courses"] = courses
        return context
class TeacherAssignmentsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/assignments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        assignments = [
            {
                "title": "Python Loops Task",
                "course": "Python",
                "due_date": "2026-04-25",
                "submissions": 20
            },
            {
                "title": "HTML Page Design",
                "course": "Web Design",
                "due_date": "2026-04-22",
                "submissions": 15
            }
        ]

        context["assignments"] = assignments
        return context

class TeacherStudentsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/students.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students = [
            {
                "name": "Kamal Perera",
                "course": "Python",
                "attendance": 80,
                "status": "ACTIVE"
            },
            {
                "name": "Nimal Silva",
                "course": "Web Design",
                "attendance": 45,
                "status": "AT RISK"
            }
        ]

        context["students"] = students
        return context

class TeacherAttendanceView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/attendance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        attendance = [
            {
                "student": "Kamal Perera",
                "course": "Python",
                "batch": "Batch A",
                "attendance": 85
            },
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "batch": "Batch B",
                "attendance": 45
            }
        ]

        context["attendance"] = attendance
        return context

class TeacherResultsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        results = [
            {
                "student": "Kamal Perera",
                "course": "Python",
                "score": 75,
                "status": "PASS"
            },
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "score": 45,
                "status": "FAIL"
            }
        ]

        context["results"] = results
        return context

class TeacherMaterialsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/materials.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        materials = [
            {
                "title": "Python Basics",
                "course": "Python",
                "type": "PDF",
                "uploaded_at": "2026-04-10"
            },
            {
                "title": "HTML Tutorial",
                "course": "Web Design",
                "type": "VIDEO",
                "uploaded_at": "2026-04-12"
            }
        ]

        context["materials"] = materials
        return context

class TeacherSubmissionsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/submissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        submissions = [
            {
                "student": "Kamal Perera",
                "assignment": "Python Loops Task",
                "submitted_at": "2026-04-15",
                "status": "SUBMITTED",
                "score": None
            },
            {
                "student": "Nimal Silva",
                "assignment": "HTML Page Design",
                "submitted_at": "2026-04-14",
                "status": "GRADED",
                "score": 75
            }
        ]

        context["submissions"] = submissions
        return context

class TeacherPerformanceView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/performance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace with real analytics later)
        performance = [
            {"student": "Kamal Perera", "course": "Python", "avg_score": 78, "attendance": 85, "status": "GOOD"},
            {"student": "Nimal Silva", "course": "Web Design", "avg_score": 45, "attendance": 50, "status": "AT RISK"},
        ]

        avg_class_score = sum(p["avg_score"] for p in performance) / len(performance)
        at_risk_count = sum(1 for p in performance if p["status"] == "AT RISK")

        context.update({
            "performance": performance,
            "avg_class_score": round(avg_class_score, 2),
            "at_risk_count": at_risk_count,
        })

        return context

class TeacherRiskStudentsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/risk_students.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace with ML later)
        risk_students = [
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "attendance": 45,
                "avg_score": 40,
                "risk_level": "HIGH"
            },
            {
                "student": "Sunil Perera",
                "course": "Python",
                "attendance": 55,
                "avg_score": 50,
                "risk_level": "MEDIUM"
            }
        ]

        high_risk = sum(1 for s in risk_students if s["risk_level"] == "HIGH")

        context.update({
            "risk_students": risk_students,
            "high_risk": high_risk,
        })

        return context


class TeacherAnalyticsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace with real queries later)
        total_students = 30
        avg_attendance = 68
        avg_score = 62
        at_risk = 5

        # Course-wise performance
        course_data = [
            {"course": "Python", "avg_score": 70},
            {"course": "Web Design", "avg_score": 55},
        ]

        context.update({
            "total_students": total_students,
            "avg_attendance": avg_attendance,
            "avg_score": avg_score,
            "at_risk": at_risk,
            "course_data": course_data,
        })

        return context


class TeacherNotificationsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        notifications = [
            {
                "message": "Nimal Silva has low attendance",
                "type": "ALERT",
                "created_at": "2026-04-17",
                "is_read": False
            },
            {
                "message": "New assignment submissions received",
                "type": "INFO",
                "created_at": "2026-04-16",
                "is_read": True
            },
            {
                "message": "3 students are at high risk",
                "type": "WARNING",
                "created_at": "2026-04-15",
                "is_read": False
            }
        ]

        unread_count = sum(1 for n in notifications if not n["is_read"])

        context.update({
            "notifications": notifications,
            "unread_count": unread_count,
        })

        return context

class TeacherMessagesView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/messages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        threads = [
            {"name": "Kamal Perera", "last_message": "Sir, I have a question", "active": True},
            {"name": "Nimal Silva", "last_message": "Thank you!", "active": False},
        ]

        messages = [
            {"sender": "student", "text": "Sir, I have a question", "timestamp": "10:00 AM"},
            {"sender": "teacher", "text": "Yes, tell me", "timestamp": "10:02 AM"},
        ]

        context.update({
            "threads": threads,
            "messages": messages,
        })

        return context

class TeacherAnnouncementsView(BaseView):
    allowed_roles = ['TEACHER']
    template_name = "dashboard/teachers/announcements.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        announcements = [
            {
                "title": "Exam Schedule",
                "message": "Final exam starts next week",
                "course": "Python",
                "priority": "HIGH",
                "created_at": "2026-04-17"
            },
            {
                "title": "New Assignment",
                "message": "Check assignments page",
                "course": "Web Design",
                "priority": "MEDIUM",
                "created_at": "2026-04-15"
            }
        ]

        context["announcements"] = announcements
        return context
