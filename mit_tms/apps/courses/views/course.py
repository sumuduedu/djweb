from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .base import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView

from ..models import Course
from ..forms import CourseForm

from .base import BaseListView
from ..services.course_service import CourseService
from apps.core.permission_engine import PermissionEngine
from django.http import HttpResponseForbidden

from apps.courses.selectors.course_selector import CourseSelector

class CourseListView(BaseListView):
    template_name = "courses/course_lists.html"

    def dispatch(self, request, *args, **kwargs):
        if not PermissionEngine.can(request.user, "course", "read"):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return CourseSelector.list(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["table"] = CourseService.get_table(self.request.user)

        # ✅ permissions INSIDE method
        context["can_create"] = PermissionEngine.can(
            self.request.user, "course", "create"
        )

        context["can_update"] = PermissionEngine.can(
            self.request.user, "course", "update"
        )

        context["can_delete"] = PermissionEngine.can(
            self.request.user, "course", "delete"
        )

        return context

from .base import BaseDetailView
from ..models import Course


class CourseDetailView(BaseDetailView):
    model = Course
    template_name = "courses/course_detail.html"

    def get_extra_context(self):
        course = self.object
        modules = course.modules.all()

        total_theory = sum(m.theory_hours or 0 for m in modules)
        total_practical = sum(m.practical_hours or 0 for m in modules)

        course_theory = course.theory_hours or 0
        course_practical = course.practical_hours or 0
        course_assignment = course.assignment_hours or 0

        return {
            # totals
            'total_theory': total_theory,
            'total_practical': total_practical,
            'total_hours_sum': total_theory + total_practical,
            'total_months': course.duration_months,

            # course values
            'course_theory': course_theory,
            'course_practical': course_practical,
            'course_industry': course_assignment,

            # details
            'course_level': course.level,
            'course_medium': course.medium,
            'delivery_mode': course.delivery_mode,
            'course_mode': course.course_mode,
            'entry_qualification': course.entry_qualification,

            'nvq_level': course.nvq_level,
            'qualification_code': course.qualification_code,

            'batches_per_year': course.batches_per_year,
            'students_per_batch': course.students_per_batch,

            'course_fee': course.course_fee,
            'is_free': course.is_free,
            'fee_includes': course.fee_includes,

            'tools': course.tools_available,
            'equipment': course.equipment_available,
            'machinery': course.machinery_available,

            'prerequisite': course.prerequisite,
            'learning_outcomes': course.learning_outcomes,

            'industry': course.industry,
            'equivalent_course': course.equivalent_course,



            # validation
            'is_matching': (
                total_theory == course_theory and
                total_practical == course_practical
            )
        }

class CourseCreateView(BaseCreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy('courses:course_list')

    success_message = "Course created successfully ✅"


class CourseUpdateView(BaseUpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy('courses:course_list')

    success_message = "Course updated successfully ✏️"

class CourseDeleteView(BaseDeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"
    success_url = reverse_lazy('courses:course_list')

    success_message = "Course deleted successfully ❌"
