from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.accounts.models import Student, Teacher
from apps.enrollment.models import Enrollment
from .models import Batch
from .forms import BatchForm


# =========================
# 📦 BATCH CRUD
# =========================

class BatchListView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = "batch/batch_list.html"
    context_object_name = "batches"

    def get_queryset(self):
        return Batch.objects.select_related('course').order_by('-created_at')


class BatchDetailView(LoginRequiredMixin, DetailView):
    model = Batch
    template_name = "batch/batch_detail.html"
    context_object_name = "batch"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        batch = self.object

        context['students'] = batch.enrollments.select_related('student')
        context['teacher'] = batch.teacher

        context['all_students'] = Student.objects.all()
        context['all_teachers'] = Teacher.objects.all()

        return context


class BatchCreateView(LoginRequiredMixin, CreateView):
    model = Batch
    form_class = BatchForm
    template_name = "batch/batch_form.html"
    success_url = reverse_lazy('batch:batch_list')

    def form_valid(self, form):
        messages.success(self.request, "Batch created successfully ✅")
        return super().form_valid(form)


class BatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = "batch/batch_form.html"

    def get_success_url(self):
        return reverse_lazy('batch:batch_detail', kwargs={'pk': self.object.pk})


class BatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Batch
    template_name = "batch/batch_confirm_delete.html"
    success_url = reverse_lazy('batch:batch_list')


# =========================
# 🎓 ASSIGN STUDENT
# =========================

class AssignStudentToBatchView(LoginRequiredMixin, View):

    def post(self, request, batch_id, student_id):
        batch = get_object_or_404(Batch, id=batch_id)
        student = get_object_or_404(Student, id=student_id)

        if Enrollment.objects.filter(student=student, batch=batch).exists():
            messages.warning(request, "Student already assigned.")
        else:
            Enrollment.objects.create(student=student, batch=batch)
            messages.success(request, "Student assigned successfully.")

        return redirect('batch:batch_detail', pk=batch_id)


# =========================
# 👨‍🏫 ASSIGN TEACHER
# =========================

class AssignTeacherView(LoginRequiredMixin, View):

    def post(self, request, batch_id):
        batch = get_object_or_404(Batch, id=batch_id)
        teacher_id = request.POST.get("teacher_id")

        teacher = get_object_or_404(Teacher, id=teacher_id)

        batch.teacher = teacher
        batch.save()

        messages.success(request, "Teacher assigned successfully.")
        return redirect('batch:batch_detail', pk=batch_id)
