# 🔷 Django core imports
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

# 🔷 Django class-based views
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

# 🔷 Auth
from django.contrib.auth.mixins import LoginRequiredMixin


# 🔷 Local app imports
from .models import Course, Module, Task, Unit
from .forms import CourseForm, ModuleForm, TaskForm, UnitForm, ElementFormSet

from django.shortcuts import redirect
# =========================================================
# 🔷 COURSE VIEWS
# =========================================================

# 📋 List Courses
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    paginate_by = 10

    def get_queryset(self):
        return Course.objects.all().order_by('-created_at')


# 🔍 Course Detail
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        modules = self.object.modules.all()

        # 🔥 MODULE TOTALS
        total_theory = sum(m.theory_hours or 0 for m in modules)
        total_practical = sum(m.practical_hours or 0 for m in modules)

        context['total_theory'] = total_theory
        context['total_practical'] = total_practical

        # 🔥 COURSE VALUES
        course_theory = self.object.theory_hours or 0
        course_practical = self.object.practical_hours or 0

        context['course_theory'] = course_theory
        context['course_practical'] = course_practical
        context['course_industry'] = self.object.industry_training_hours or 0
        context['total_hours_sum'] = total_theory + total_practical
        # 🔥 MONTHS
        context['total_months'] = self.object.duration_months

        # 🔥 ✅ MATCH CHECK (NEW)
        context['is_matching'] = (
            total_theory == course_theory and
            total_practical == course_practical
        )

        return context


# ➕ Create Course
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, "Course created successfully ✅")
        return super().form_valid(form)


# ✏️ Update Course
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, "Course updated successfully ✏️")
        return super().form_valid(form)


# ❌ Delete Course
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"
    success_url = reverse_lazy('course_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Course deleted successfully ❌")
        return super().delete(request, *args, **kwargs)


# =========================================================
# 🔥 MODULE VIEWS
# =========================================================

# ➕ Create Module
class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "courses/module_form.html"

    def form_valid(self, form):
        # 🔥 Automatically assign course
        form.instance.course_id = self.kwargs['course_id']
        messages.success(self.request, "Module created successfully ✅")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})


# ✏️ Update Module
class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = "courses/module_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Module updated successfully ✏️")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})

class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = "courses/module_detail.html"
    context_object_name = "module"


# ❌ Delete Module
class ModuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Module
    template_name = "courses/module_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Module deleted successfully ❌")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "courses/task_form.html"

    def form_valid(self, form):
        form.instance.module_id = self.kwargs['module_id']
        messages.success(self.request, "Task created successfully ✅")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('module_detail', kwargs={'pk': self.object.module.pk})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "courses/task_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully ✏️")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('module_detail', kwargs={'pk': self.object.module.pk})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "courses/task_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task deleted successfully ❌")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('module_detail', kwargs={'pk': self.object.module.pk})


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "courses/task_detail.html"
    context_object_name = "task"


class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = "courses/unit_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['elements'] = ElementFormSet(self.request.POST)
        else:
            data['elements'] = ElementFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        elements = context['elements']

        # 🔥 SET COURSE BEFORE VALIDATION
        form.instance.course_id = self.kwargs['course_id']

        if elements.is_valid():
            self.object = form.save()
            elements.instance = self.object
            elements.save()

            messages.success(self.request, "Unit + Elements created successfully ✅")
            return redirect(self.get_success_url())

        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})

class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = "courses/unit_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Unit updated successfully ✏️")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})


class UnitDeleteView(LoginRequiredMixin, DeleteView):
    model = Unit
    template_name = "courses/unit_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Unit deleted successfully ❌")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})

class UnitDetailView(LoginRequiredMixin, DetailView):
    model = Unit
    template_name = "courses/unit_detail.html"
    context_object_name = "unit"

class CourseNCSView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_ncs.html"
    context_object_name = "course"


from django.http import JsonResponse
from .models import Module
from django.http import JsonResponse
from .models import Module

from django.http import JsonResponse
from .models import Module

def get_module_details(request):
    code = request.GET.get('code')

    module = Module.objects.filter(code=code).first()

    if module:
        data = {
            'title': module.title,
            'description': module.description,
            'module_type': module.module_type,

            'total_hours': module.total_hours,
            'theory_hours': module.theory_hours,
            'practical_hours': module.practical_hours,

            'learning_outcomes': module.learning_outcomes,
            'theory_content': module.theory_content,
            'practical_content': module.practical_content,

            'teaching_methods': module.teaching_methods,
            'assessment_methods': module.assessment_methods,

            'order': module.order,
        }
    else:
        data = {}

    return JsonResponse(data)
