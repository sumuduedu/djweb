from .base import BaseView


class ParentDashboardView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parent.html"

class ParentChildrenView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parents/children.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        children = [
            {
                "name": "Kamal Perera",
                "course": "Python",
                "batch": "Batch A",
                "status": "ACTIVE"
            },
            {
                "name": "Nimal Silva",
                "course": "Web Design",
                "batch": "Batch B",
                "status": "ACTIVE"
            }
        ]

        context["children"] = children
        return context

class ParentProgressView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parents/progress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        progress = [
            {
                "student": "Kamal Perera",
                "course": "Python",
                "attendance": 85,
                "avg_score": 78,
                "status": "GOOD"
            },
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "attendance": 50,
                "avg_score": 45,
                "status": "AT RISK"
            }
        ]

        context["progress"] = progress
        return context

class ParentAttendanceView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parents/attendance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        attendance = [
            {
                "student": "Kamal Perera",
                "course": "Python",
                "attendance": 85,
                "status": "GOOD"
            },
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "attendance": 45,
                "status": "LOW"
            }
        ]

        context["attendance"] = attendance
        context["low_count"] = sum(1 for a in attendance if a["attendance"] < 50)

        return context

class ParentPaymentsView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parents/payments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        payments = [
            {
                "student": "Kamal Perera",
                "course": "Python",
                "amount": 15000,
                "date": "2026-04-10",
                "status": "PAID"
            },
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "amount": 12000,
                "date": "2026-04-15",
                "status": "PENDING"
            }
        ]

        context["payments"] = payments
        context["total_paid"] = sum(p["amount"] for p in payments if p["status"] == "PAID")
        context["pending"] = sum(1 for p in payments if p["status"] == "PENDING")

        return context


class ParentResultsView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parents/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        results = [
            {
                "student": "Kamal Perera",
                "course": "Python",
                "score": 78,
                "status": "PASS"
            },
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "score": 45,
                "status": "FAIL"
            }
        ]

        # Summary
        avg_score = sum(r["score"] for r in results) / len(results)
        failed = sum(1 for r in results if r["status"] == "FAIL")

        context.update({
            "results": results,
            "avg_score": round(avg_score, 2),
            "failed": failed,
        })

        return context

class ParentMessagesView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parents/messages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        threads = [
            {"name": "Mr. Silva (Teacher)", "last_message": "Your child needs improvement", "active": True},
            {"name": "Ms. Perera (Teacher)", "last_message": "Great progress!", "active": False},
        ]

        messages = [
            {"sender": "parent", "text": "How is my child doing?", "time": "09:00 AM"},
            {"sender": "teacher", "text": "Needs to improve attendance", "time": "09:10 AM"},
        ]

        context.update({
            "threads": threads,
            "messages": messages,
        })

        return context

class ParentNotificationsView(BaseView):
    allowed_roles = ['PARENT']
    template_name = "dashboard/parents/notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        notifications = [
            {
                "message": "Your child has low attendance",
                "type": "ALERT",
                "created_at": "2026-04-17",
                "is_read": False
            },
            {
                "message": "New exam results available",
                "type": "INFO",
                "created_at": "2026-04-16",
                "is_read": True
            },
            {
                "message": "Payment is pending",
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
