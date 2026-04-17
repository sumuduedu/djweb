from .base import BaseView
from django.contrib.auth.models import User
from apps.accounts.models import Student, Teacher
from apps.enrollment.models import EnrollmentInquiry, Enrollment
from apps.website.models import ContactMessage
from apps.batch.models import Batch


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
