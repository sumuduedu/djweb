from .base import *
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
from apps.courses.models.module import *

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

class AdminCourseListView(BaseView):
    template_name = "admin/courses/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_year = now().year

        courses = Course.objects.all().order_by("-created_at")

        context["courses"] = courses

        context["total_courses"] = courses.count()

        context["current_year_courses"] = Course.objects.filter(
            created_at__year=current_year
        ).count()

        context["total_students_enrolled"] = Enrollment.objects.count()

        # ✅ FIXED
        context["active_courses"] = Course.objects.filter(
            status='ACTIVE'
        ).count()

        context["current_ncs_version"] = NCS.objects.filter(
            is_active=True
        ).first()

        context["old_ncs_count"] = NCS.objects.filter(
            is_active=False
        ).count()

        return context

class AdminCourseDetailView(BaseDetailView):
    model = Course
    template_name = "admin/courses/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.object
        modules = course.modules.all()

        total_theory = sum(m.theory_hours or 0 for m in modules)
        total_practical = sum(m.practical_hours or 0 for m in modules)

        course_theory = course.theory_hours or 0
        course_practical = course.practical_hours or 0
        course_assignment = course.assignment_hours or 0

        context.update({
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
        })

        return context

from django.urls import reverse_lazy
from apps.courses.models import Course
from .base import BaseCreateView

from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from apps.courses.models import Course
from apps.courses.models.resource import *
from .base import BaseCreateView

from django.forms import inlineformset_factory

ResourceFormSet = inlineformset_factory(
    Course,
    LearningResource,   # ✅ FIXED
    fields=('name', 'type', 'file', 'url', 'description'),
    extra=1,
    can_delete=True
)
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from apps.courses.models import Course
from apps.courses.models.resource import LearningResource
from .base import BaseCreateView


# ✅ Correct Formset (NO empty forms)
LearningResourceFormSet = inlineformset_factory(
    Course,
    LearningResource,
    fields=('name', 'type', 'file', 'url', 'description'),
    extra=1,   # ✅ IMPORTANT
    can_delete=True
)


class AdminCourseCreateView(BaseCreateView):
    model = Course
    template_name = "admin/courses/form.html"
    fields = '__all__'
    success_url = reverse_lazy('dashboard:admin_courses_list')

    allowed_roles = ['ADMIN']
    success_message = "Course created successfully 🎉"

    # ✅ Add formset to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['resource_formset'] = LearningResourceFormSet(
                self.request.POST,
                self.request.FILES
            )
        else:
            context['resource_formset'] = LearningResourceFormSet()

        return context

    # ✅ Save course + resources safely
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['resource_formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object

            for f in formset:
                # ✅ Ignore completely empty forms
                if not f.cleaned_data:
                    continue

                # ❌ Skip incomplete forms (no name)
                if not f.cleaned_data.get('name'):
                    continue

                f.save()

            return super().form_valid(form)

        return self.form_invalid(form)

from django.urls import reverse_lazy
from apps.courses.models import Course
from .base import BaseUpdateView


class AdminCourseUpdateView(BaseUpdateView):
    model = Course
    template_name = "admin/courses/form.html"
    fields = '__all__'
    success_url = reverse_lazy('dashboard:admin_courses')

    allowed_roles = ['ADMIN']

    success_message = "Course updated successfully ✏️"

from django.urls import reverse_lazy
from apps.courses.models import Course
from .base import BaseDeleteView


class AdminCourseDeleteView(BaseDeleteView):
    model = Course
    template_name = "admin/courses/delete.html"
    success_url = reverse_lazy('dashboard:admin_courses_list')

    allowed_roles = ['ADMIN']

    success_message = "Course deleted successfully 🗑"


from django.urls import reverse_lazy
from apps.courses.models import Unit   # Module = Unit
from .base import BaseDetailView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseView


class AdminModuleListView(BaseView):
    template_name = "admin/modules/list.html"
    allowed_roles = ['ADMIN']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context["modules"] = modules
        context["total_modules"] = modules.count()

        return context

from .base import BaseDetailView
from apps.courses.models.module import Module

class AdminModuleDetailView(BaseDetailView):
    model = Module
    template_name = "admin/modules/detail.html"
    allowed_roles = ['ADMIN']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        module = self.object

        context.update({
            'course': module.course,

            # Hours summary
            'total_hours': module.total_hours or 0,
            'theory_hours': module.theory_hours or 0,
            'practical_hours': module.practical_hours or 0,

            # Content
            'learning_outcomes': module.learning_outcomes,
            'theory_content': module.theory_content,
            'practical_content': module.practical_content,

            # Methods
            'teaching_methods': module.teaching_methods,
            'assessment_methods': module.assessment_methods,
        })

        return context


class AdminModuleCreateView(BaseCreateView):
    model = Module
    template_name = "admin/modules/form.html"
    fields = [
        'code', 'title', 'description', 'module_type',
        'duration_months', 'total_hours', 'theory_hours', 'practical_hours',
        'learning_outcomes', 'theory_content', 'practical_content',
        'teaching_methods', 'assessment_methods', 'order',
    ]

    allowed_roles = ['ADMIN']
    success_message = "Module created successfully 🎉"

    # ✅ SAFE: works with course_id OR pk
    def get_course_id(self):
        return self.kwargs.get('course_id') or self.kwargs.get('pk')

    def form_valid(self, form):
        course_id = self.get_course_id()
        form.instance.course_id = course_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course_id = self.get_course_id()

        if course_id:
            context['course'] = Course.objects.get(id=course_id)

        return context

    def get_success_url(self):
        return reverse_lazy(
            'dashboard:admin_course_detail',
            kwargs={'pk': self.object.course.id}
        )

class AdminModuleUpdateView(BaseUpdateView):
    model = Module   # ✅ FIXED
    template_name = "admin/modules/form.html"
    fields = [
        'code', 'title', 'description', 'module_type',
        'duration_months', 'total_hours', 'theory_hours', 'practical_hours',
        'learning_outcomes', 'theory_content', 'practical_content',
        'teaching_methods', 'assessment_methods', 'order',
    ]

    allowed_roles = ['ADMIN']
    success_message = "Module updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy(
            'dashboard:admin_course_detail',
            kwargs={'pk': self.object.course.id}
        )


class AdminModuleDeleteView(BaseDeleteView):
    model = Module   # ✅ FIXED
    template_name = "admin/modules/delete.html"
    allowed_roles = ['ADMIN']

    success_message = "Module deleted successfully 🗑"

    def get_success_url(self):
        return reverse_lazy(
            'dashboard:admin_course_detail',
            kwargs={'pk': self.object.course.id}
        )
from apps.courses.models import Element

class AdminTaskListView(BaseView):
    template_name = "admin/tasks/list.html"
    allowed_roles = ['ADMIN']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        module_id = self.kwargs.get('module_id')

        tasks = Element.objects.select_related("module").filter(
            module_id=module_id
        ).order_by("-id")

        context["tasks"] = tasks
        context["total_tasks"] = tasks.count()
        context["module"] = Module.objects.get(id=module_id)

        return context

class AdminTaskDetailView(BaseDetailView):
    model = Element
    template_name = "admin/tasks/detail.html"
    allowed_roles = ['ADMIN']
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
class AdminTaskCreateView(BaseCreateView):
    model = Element
    template_name = "admin/tasks/form.html"
    fields = ['title', 'description', 'order']

    allowed_roles = ['ADMIN']
    success_message = "Task created successfully 🎉"

    def get_module(self):
        module_id = self.kwargs.get('module_id')
        return get_object_or_404(Module, id=module_id)

    def dispatch(self, request, *args, **kwargs):
        self.module = self.get_module()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.module = self.module
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module
        return context

    def get_success_url(self):
        return reverse_lazy(
            'dashboard:admin_task_list',
            kwargs={'module_id': self.module.id}
        )

class AdminTaskUpdateView(BaseUpdateView):
    model = Element
    template_name = "admin/tasks/form.html"
    fields = [
        'title', 'description', 'order'
    ]

    allowed_roles = ['ADMIN']
    success_message = "Task updated successfully ✏️"

    def get_success_url(self):
        return reverse_lazy(
            'dashboard:admin_task_list',
            kwargs={'module_id': self.object.module.id}
        )
class AdminTaskDeleteView(BaseDeleteView):
    model = Element
    template_name = "admin/tasks/delete.html"
    allowed_roles = ['ADMIN']

    success_message = "Task deleted successfully 🗑"

    def get_success_url(self):
        return reverse_lazy(
            'dashboard:admin_task_list',
            kwargs={'module_id': self.object.module.id}
        )

from apps.courses.models import Activity


class AdminActivityListView(BaseView):
    template_name = "admin/activities/list.html"
    allowed_roles = ['ADMIN']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        activities = Activity.objects.select_related("element").all().order_by("-id")

        context["activities"] = activities
        context["total_activities"] = activities.count()

        return context


class AdminActivityDetailView(BaseDetailView):
    model = Activity
    template_name = "admin/activities/detail.html"
    allowed_roles = ['ADMIN']


class AdminActivityCreateView(BaseCreateView):
    model = Activity
    template_name = "admin/activities/form.html"
    fields = '__all__'
    success_url = reverse_lazy('dashboard:admin_activities')
    allowed_roles = ['ADMIN']

    success_message = "Activity created successfully 🎉"


class AdminActivityUpdateView(BaseUpdateView):
    model = Activity
    template_name = "admin/activities/form.html"
    fields = '__all__'
    success_url = reverse_lazy('dashboard:admin_activities')
    allowed_roles = ['ADMIN']

    success_message = "Activity updated successfully ✏️"


class AdminActivityDeleteView(BaseDeleteView):
    model = Activity
    template_name = "admin/activities/delete.html"
    success_url = reverse_lazy('dashboard:admin_activities')
    allowed_roles = ['ADMIN']

    success_message = "Activity deleted successfully 🗑"
