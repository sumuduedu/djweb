from .base import BaseView
from apps.enrollment.models import EnrollmentInquiry


class StaffDashboardView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pending'] = EnrollmentInquiry.objects.filter(status='PENDING').count()
        context['approved'] = EnrollmentInquiry.objects.filter(status='APPROVED').count()
        context['rejected'] = EnrollmentInquiry.objects.filter(status='REJECTED').count()

        return context

class StaffStudentsView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff/students.html"

class StaffPaymentsView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff/payments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA
        payments = [
            {
                "student": "Kamal Perera",
                "course": "Python",
                "amount": 15000,
                "method": "Cash",
                "date": "2026-04-10",
                "status": "PAID"
            },
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "amount": 12000,
                "method": "Bank Transfer",
                "date": "2026-04-12",
                "status": "PENDING"
            }
        ]

        context["payments"] = payments
        return context

class StaffEnrollmentsView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff/enrollments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later with model)
        enrollments = [
            {
                "student": "Kamal Perera",
                "course": "Python",
                "batch": "Batch A",
                "status": "ACTIVE",
                "date": "2026-04-01"
            },
            {
                "student": "Nimal Silva",
                "course": "Web Design",
                "batch": "Batch B",
                "status": "PENDING",
                "date": "2026-04-05"
            }
        ]
class StaffReportsView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        reports = {
            "total_students": 120,
            "active_courses": 8,
            "monthly_income": 250000,
            "pending_payments": 5,
        }

        context["reports"] = reports
        return context

        context["enrollments"] = enrollments
        context["total"] = len(enrollments)
        context["active"] = sum(1 for e in enrollments if e["status"] == "ACTIVE")
        context["pending"] = sum(1 for e in enrollments if e["status"] == "PENDING")

        return context

class StaffBatchesView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff/batches.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        batches = [
            {
                "name": "Batch A",
                "course": "Python Programming",
                "teacher": "Mr. Silva",
                "students": 25,
                "start_date": "2026-04-01",
                "status": "ACTIVE"
            },
            {
                "name": "Batch B",
                "course": "Web Design",
                "teacher": "Ms. Perera",
                "students": 18,
                "start_date": "2026-03-15",
                "status": "COMPLETED"
            }
        ]

        context["batches"] = batches
        context["total"] = len(batches)
        context["active"] = sum(1 for b in batches if b["status"] == "ACTIVE")

        return context


class StaffAttendanceView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff/attendance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        attendance = [
            {
                "student": "Kamal Perera",
                "batch": "Batch A",
                "course": "Python",
                "attendance": 85,
                "status": "GOOD"
            },
            {
                "student": "Nimal Silva",
                "batch": "Batch B",
                "course": "Web Design",
                "attendance": 45,
                "status": "LOW"
            },
        ]

        context["attendance"] = attendance
        context["total"] = len(attendance)
        context["low"] = sum(1 for a in attendance if a["attendance"] < 50)

        return context

class StaffInvoicesView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff/invoices.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        invoices = [
            {
                "invoice_no": "INV-001",
                "student": "Kamal Perera",
                "course": "Python",
                "amount": 15000,
                "due_date": "2026-04-20",
                "status": "UNPAID"
            },
            {
                "invoice_no": "INV-002",
                "student": "Nimal Silva",
                "course": "Web Design",
                "amount": 12000,
                "due_date": "2026-04-10",
                "status": "PAID"
            }
        ]

        context["invoices"] = invoices
        context["total"] = len(invoices)
        context["unpaid"] = sum(1 for i in invoices if i["status"] == "UNPAID")
        context["paid"] = sum(1 for i in invoices if i["status"] == "PAID")

        return context
class StaffNotificationsView(BaseView):
    allowed_roles = ['STAFF']
    template_name = "dashboard/staff/notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later)
        notifications = [
            {
                "message": "Kamal Perera has low attendance",
                "type": "ALERT",
                "created_at": "2026-04-17",
                "is_read": False
            },
            {
                "message": "New enrollment request received",
                "type": "INFO",
                "created_at": "2026-04-16",
                "is_read": True
            },
            {
                "message": "5 students have pending payments",
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

