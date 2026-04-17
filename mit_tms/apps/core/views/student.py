from .base import BaseView
from apps.core.gateway import get_student_enrollments
from apps.enrollment.models import EnrollmentInquiry


# ================================
# 🎓 DASHBOARD
# ================================
class StudentDashboardView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/student.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['enrollments'] = get_student_enrollments(user)
        context['approved_apps'] = EnrollmentInquiry.objects.filter(
            user=user, status='APPROVED'
        )

        return context


# ================================
# 📚 COURSES
# ================================
class StudentCoursesView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = get_student_enrollments(self.request.user)
        return context


# ================================
# 📅 ATTENDANCE
# ================================
class StudentAttendanceView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/attendance.html"


# ================================
# 💳 PAYMENTS
# ================================
class StudentPaymentView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/payment.html"


# ================================
# 📝 ASSIGNMENTS
# ================================
class StudentAssignmentsView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/assignments.html"


# ================================
# 🏆 RESULTS
# ================================
class StudentResultsView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/results.html"


# ================================
# 📈 PROGRESS
# ================================
class StudentProgressView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/progress.html"


# ================================
# 🔔 NOTIFICATIONS
# ================================
class StudentNotificationsView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/notifications.html"


# ================================
# 📂 MATERIALS
# ================================
class StudentMaterialsView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/materials.html"


# ================================
# 🎓 CERTIFICATES
# ================================
class StudentCertificateView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/certificates.html"


# ================================
# 💬 MESSAGES
# ================================
class StudentMessagesView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/messages.html"


# ================================
# 📢 ANNOUNCEMENTS
# ================================
class StudentAnnouncementsView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/announcements.html"


# ================================
# 🧾 RECEIPTS
# ================================
class StudentReceiptsView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/receipts.html"


# ================================
# 🧠 INSIGHTS (🔥 IMPORTANT)
# ================================
class StudentInsights(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/insights.html"

# ================================
# ⚠️ STUDENT RISK (🔥 IMPORTANT)
# ================================
class StudentRiskView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/risk.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # 🔥 TEMP LOGIC (replace with ML later)
        attendance = 60   # example
        progress = 50     # example

        # Simple rule-based risk (temporary)
        if attendance < 50 or progress < 40:
            risk_level = "HIGH"
        elif attendance < 70:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        context.update({
            "risk_level": risk_level,
            "attendance": attendance,
            "progress": progress,
        })

        return context

# ================================
# 💡 STUDENT RECOMMENDATIONS (🔥 IMPORTANT)
# ================================
class StudentRecommendationsView(BaseView):
    allowed_roles = ['STUDENT']
    template_name = "dashboard/students/recommendations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 TEMP DATA (replace later with real + ML)
        attendance = 55
        progress = 45
        pending_tasks = 3

        recommendations = []

        # Rule-based recommendations (for now)
        if attendance < 60:
            recommendations.append("Improve attendance by attending all sessions")

        if progress < 50:
            recommendations.append("Focus on completing pending modules")

        if pending_tasks > 0:
            recommendations.append("Complete all pending assignments")

        if not recommendations:
            recommendations.append("Keep up the good performance 🎉")

        context.update({
            "attendance": attendance,
            "progress": progress,
            "pending_tasks": pending_tasks,
            "recommendations": recommendations,
        })

        return context
