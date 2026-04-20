from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import LessonPlan
from .forms import LessonPlanForm, LessonActivityFormSet


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
            return LessonPlan.objects.select_related("task__module__course").all()

        teacher = getattr(user, "teacher", None)

        if teacher:
            return LessonPlan.objects.filter(instructor=teacher)

        return LessonPlan.objects.none()


# ================================
# 📄 DETAIL VIEW
# ================================
class LessonDetailView(LoginRequiredMixin, IsOwnerOrAdminMixin, DetailView):
    model = LessonPlan
    template_name = "lessonplan/detail.html"
    context_object_name = "lesson"


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

    def form_valid(self, form):
        context = self.get_context_data()
        activities = context["activities"]

        teacher = getattr(self.request.user, "teacher", None)

        if teacher:
            form.instance.instructor = teacher   # ✅ FIXED

        if activities.is_valid():
            self.object = form.save()
            activities.instance = self.object
            activities.save()
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
            data["activities"] = LessonActivityFormSet(self.request.POST, instance=self.object)
        else:
            data["activities"] = LessonActivityFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        activities = context["activities"]

        if activities.is_valid():
            self.object = form.save()
            activities.instance = self.object
            activities.save()
            return redirect(self.success_url)

        return self.form_invalid(form)


# ================================
# 🗑️ DELETE VIEW
# ================================
class LessonDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    model = LessonPlan
    template_name = "lessonplan/delete.html"
    success_url = reverse_lazy("lessonplan:list")
