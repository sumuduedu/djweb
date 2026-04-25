from .base import BaseView
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from django.utils.timezone import now
from django.db.models import Count
from apps.courses.models import Course, Unit, Element, Activity
from apps.accounts.models import Student, Teacher
from apps.enrollment.models import EnrollmentInquiry, Enrollment
from apps.website.models import ContactMessage
from apps.batch.models import Batch
from apps.courses.models import  NCS
class AdminDashboardView(BaseView):
    allowed_roles = ['ADMIN']
    template_name = "dashboard/admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_users'] = User.objects.count()
        context['total_students'] = Student.objects.count()
        context['total_teachers'] = Teacher.objects.count()
        context['pending_applications'] = EnrollmentInquiry.objects.filter(status='PENDING').count()

        context['total_batches'] = Batch.objects.count()
        context['total_enrollments'] = Enrollment.objects.count()

        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        context['applications'] = EnrollmentInquiry.objects.order_by('-created_at')[:5]
        context['messages'] = ContactMessage.objects.order_by('-created_at')[:5]

        context['enrollments'] = Enrollment.objects.select_related(
            'student', 'batch__course'
        ).order_by('-enrolled_at')[:5]

        context['new_messages'] = ContactMessage.objects.filter(is_read=False).count()

        return context


class AdminCourseView(BaseView):
    template_name = "dashboard/admin/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_year = now().year

        context["current_year_courses"] = Course.objects.filter(
            created_at__year=current_year
        ).count()

        context["total_students_enrolled"] = Enrollment.objects.count()

        # if is_active exists
        context["active_courses"] = Course.objects.filter(
            is_active=True
        ).count() if hasattr(Course, "is_active") else 0

        context["current_ncs_version"] = NCS.objects.filter(
            is_active=True
        ).first()

        context["old_ncs_count"] = NCS.objects.filter(
            is_active=False
        ).count()

        return context
