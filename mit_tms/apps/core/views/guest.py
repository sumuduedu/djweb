from .base import BaseView
from apps.courses.models import Course
from apps.enrollment.models import EnrollmentInquiry


class GuestDashboardView(BaseView):
    allowed_roles = ['GUEST']
    template_name = "dashboard/guest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        courses = list(Course.objects.all())

        user_apps = EnrollmentInquiry.objects.filter(
            user=self.request.user
        ).select_related('course')

        # 🔥 map applications
        app_map = {app.course_id: app for app in user_apps}

        # 🔥 attach application to each course
        for course in courses:
            course.application = app_map.get(course.id)

        context['courses'] = courses
        context['applications'] = app_map  # keep if needed

        return context
