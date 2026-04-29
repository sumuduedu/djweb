from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.db import transaction
import json

from apps.courses.models import Task
from .models import LessonPlan, LessonActivity
from .forms import LessonPlanForm, LessonActivityFormSet

# ✅ NEW: smart generator import
from .services import generate_lesson_plan, generate_smart_lesson_plan


# ================================
# 🔐 PERMISSION MIXIN
# ================================
class IsOwnerOrAdminMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        teacher = getattr(self.request.user, "teacher", None)

        return (
            self.request.user.is_staff or
            (teacher and obj.instructor == teacher)
        )


# ================================
# 📘 LIST VIEW
# ================================
class LessonListView(LoginRequiredMixin, ListView):
    model = LessonPlan
    template_name = "lessonplan/list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return LessonPlan.objects.select_related(
                "task__module__course"
            ).prefetch_related("activities")

        teacher = getattr(user, "teacher", None)

        if teacher:
            return LessonPlan.objects.select_related(
                "task__module__course"
            ).prefetch_related("activities").filter(instructor=teacher)

        return LessonPlan.objects.none()


# ================================
# 📄 DETAIL VIEW
# ================================
class LessonDetailView(LoginRequiredMixin, IsOwnerOrAdminMixin, DetailView):
    model = LessonPlan
    template_name = "lessonplan/detail.html"
    context_object_name = "lesson"

    # ✅ NEW: analytics
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lesson = self.object

        total = sum(a.total_time for a in lesson.activities.all())
        trainer = sum(a.trainer_time for a in lesson.activities.all())
        trainee = sum(a.trainee_time for a in lesson.activities.all())

        context["analytics"] = {
            "trainer_ratio": int((trainer / total) * 100) if total else 0,
            "trainee_ratio": int((trainee / total) * 100) if total else 0,
        }

        return context


# ================================
# ➕ CREATE VIEW
# ================================
class LessonCreateView(LoginRequiredMixin, CreateView):
    model = LessonPlan
    form_class = LessonPlanForm
    template_name = "lessonplan/form.html"
    success_url = reverse_lazy("lessonplan:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data["activities"] = LessonActivityFormSet(self.request.POST)
        else:
            data["activities"] = LessonActivityFormSet()

        return data

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        activities = context["activities"]

        teacher = getattr(self.request.user, "teacher", None)

        if teacher:
            form.instance.instructor = teacher

        if form.instance.task:
            form.instance.subject = form.instance.task.module.title

        form.instance.competency_level = "basic"
        form.instance.status = "draft"

        if activities.is_valid():
            self.object = form.save()

            for activity_form in activities:
                data = activity_form.cleaned_data

                if data and not data.get("DELETE", False):
                    activity = activity_form.save(commit=False)
                    activity.lesson = self.object
                    activity.save()

            return redirect(self.success_url)

        return self.form_invalid(form)


# ================================
# ✏️ UPDATE VIEW
# ================================
class LessonUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    model = LessonPlan
    form_class = LessonPlanForm
    template_name = "lessonplan/form.html"
    success_url = reverse_lazy("lessonplan:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data["activities"] = LessonActivityFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            data["activities"] = LessonActivityFormSet(
                instance=self.object
            )

        return data

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        activities = context["activities"]

        if form.instance.task:
            form.instance.subject = form.instance.task.module.title

        form.instance.competency_level = "basic"
        form.instance.status = "updated"

        if activities.is_valid():
            self.object = form.save()

            existing_ids = []

            for activity_form in activities:
                data = activity_form.cleaned_data

                if data and not data.get("DELETE", False):
                    activity = activity_form.save(commit=False)
                    activity.lesson = self.object
                    activity.save()
                    existing_ids.append(activity.id)

            # ✅ safer delete
            self.object.activities.exclude(id__in=existing_ids).delete()

            return redirect(self.success_url)

        return self.form_invalid(form)


# ================================
# 🗑️ DELETE VIEW
# ================================
class LessonDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = LessonPlan
    template_name = "lessonplan/delete.html"
    success_url = reverse_lazy("lessonplan:list")


# ================================
# ⚡ GENERATE LESSON
# ================================
class GenerateLessonView(LoginRequiredMixin, View):

    # ✅ FIX: POST instead of GET
    def post(self, request, *args, **kwargs):

        teacher = getattr(request.user, "teacher", None)

        if not (request.user.is_staff or teacher):
            raise PermissionDenied

        task = get_object_or_404(Task, id=kwargs.get("task_id"))

        mode = request.POST.get("mode", "basic")

        # ✅ NEW: smart mode
        if mode == "smart":
            lesson = generate_smart_lesson_plan(task, instructor=teacher)
        else:
            lesson = generate_lesson_plan(task, instructor=teacher)

        return redirect("lessonplan:detail", pk=lesson.id)


# ================================
# 🔄 AJAX: LOAD TASKS
# ================================
class LoadTasksView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        module_id = request.GET.get('module_id')

        if not module_id:
            return JsonResponse([], safe=False)

        tasks = Task.objects.filter(
            module_id=module_id
        ).order_by('title').values('id', 'title')

        return JsonResponse(list(tasks), safe=False)


# ================================
# 🧱 DRAG BUILDER
# ================================
class LessonBuilderView(DetailView):
    model = LessonPlan
    template_name = "lessonplan/drag_builder.html"
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ✅ FIX: removed invalid field "phase"
        activities = self.object.activities.all().values(
            "id", "title", "method", "order"
        )

        context["activities_json"] = json.dumps(list(activities))

        return context


# ================================
# 🔄 UPDATE ORDER (AJAX)
# ================================
class UpdateActivityOrderView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        teacher = getattr(request.user, "teacher", None)

        for item in data:
            activity = LessonActivity.objects.get(id=item["id"])

            # ✅ SECURITY FIX
            if not (request.user.is_staff or activity.lesson.instructor == teacher):
                raise PermissionDenied

            activity.order = item["order"]
            activity.save()

        return JsonResponse({"status": "ok"})


# ================================
# 🖨 PRINT VIEW
# ================================
class LessonPrintView(DetailView):
    model = LessonPlan
    template_name = "lessonplan/print.html"
    context_object_name = "lesson"

    def get_queryset(self):
        return LessonPlan.objects.select_related(
            "task__module",
            "instructor"
        ).prefetch_related(
            "activities",
            "outcomes"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activities"] = self.object.activities.all().order_by("order")
        return context
