from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import timedelta

from .models import Batch, ModulePlan, Timetable
from .forms import BatchForm, ModulePlanForm
from .utils import get_monthly_plan, generate_timetable

# =========================================================
# 🔷 BATCH VIEWS
# =========================================================

class BatchListView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = "batch/batch_list.html"
    context_object_name = "batches"
    paginate_by = 10

    def get_queryset(self):
        return Batch.objects.select_related('course').order_by('-created_at')


class BatchDetailView(LoginRequiredMixin, DetailView):
    model = Batch
    template_name = "batch/batch_detail.html"
    context_object_name = "batch"

    def get_queryset(self):
        return Batch.objects.select_related('course').prefetch_related('plans', 'timetable')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['monthly_plan'] = get_monthly_plan(self.object)
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

    def form_valid(self, form):
        messages.success(self.request, "Batch updated successfully ✏️")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('batch:batch_detail', kwargs={'pk': self.object.pk})


class BatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Batch
    template_name = "batch/batch_confirm_delete.html"
    success_url = reverse_lazy('batch:batch_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Batch deleted successfully ❌")
        return super().delete(request, *args, **kwargs)


# =========================================================
# 🔷 TIMETABLE GENERATE
# =========================================================

def generate_timetable_view(request, pk):
    batch = get_object_or_404(Batch, pk=pk)

    if batch.timetable.exists():
        messages.warning(request, "Timetable already exists ⚠️")
        return redirect('batch:batch_detail', pk=pk)

    generate_timetable(batch)

    messages.success(request, "Timetable generated successfully ✅")
    return redirect('batch:batch_detail', pk=pk)


# =========================================================
# 🔷 MODULE PLAN
# =========================================================

class ModulePlanCreateView(LoginRequiredMixin, CreateView):
    model = ModulePlan
    form_class = ModulePlanForm
    template_name = 'batch/module_plan_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(Batch, pk=self.kwargs['batch_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.batch = self.batch
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch'] = self.batch
        return context

    def get_success_url(self):
        return reverse_lazy('batch:batch_detail', kwargs={'pk': self.batch.pk})

from .models import TimeSlot
# =========================================================
# 🔷 GANTT VIEW
# =========================================================
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Batch, TimeSlot

class GanttView(View):

    def get(self, request):

        batch_id = request.GET.get("batch")
        batch = get_object_or_404(Batch, id=batch_id)

        slots = TimeSlot.objects.all().order_by("order")

        return render(request, "batch/gantt.html", {
            "batch": batch,
            "modules": batch.course.modules.all(),
            "slots": slots
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        batch_id = self.request.GET.get("batch")

        # 🔥 IMPORTANT FIX
        if not batch_id:
            # fallback → take first batch
            batch = Batch.objects.first()
        else:
            batch = get_object_or_404(Batch, id=batch_id)

        context["batch"] = batch
        context["modules"] = batch.course.modules.all()

        return context




# =========================================================
# 🔷 API
# =========================================================

def load_modules(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)

    modules = batch.course.modules.all()

    data = []
    for m in modules:
        data.append({
            "id": m.id,
            "name": m.code,
            "title": m.title,
            "hours": getattr(m, "total_hours", 0),
        })

    return JsonResponse(data, safe=False)

import json
from django.http import JsonResponse
from datetime import timedelta
from .models import Timetable, Batch
@csrf_exempt   # 🔥 IMPORTANT (for now)
def save_timetable(request):

    data = json.loads(request.body)

    batch = get_object_or_404(Batch, id=data["batch"])

    week = int(data["week"])
    day = int(data["day"])
    slot = int(data["slot"])

    # =========================
    # DELETE
    # =========================
    if data.get("delete"):

        Timetable.objects.filter(
            batch=batch,
            week=week,
            day=day,
            row_slot=slot,
            module_id=data.get("module")
        ).delete()

        return JsonResponse({"status": "deleted"})

    # =========================
    # DATE CALC
    # =========================
    total_days = (week - 1) * batch.days_per_week + (day - 1)
    class_date = batch.start_date + timedelta(days=total_days)

    # =========================
    # CREATE / UPDATE
    # =========================
    Timetable.objects.filter(
        batch=batch,
        week=week,
        day=day,
        row_slot=slot
    ).delete()

    session_type = data.get("session_type", "THEORY")

    start_time = data.get("start_time")
    end_time = data.get("end_time")

    fmt = "%H:%M"
    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)

    slot_hours = (end - start).seconds / 3600

    Timetable.objects.create(
        batch=batch,
        module_id=data["module"],
        week=week,
        day=day,
        slot_id=slot_id,
        date=class_date,
        hours=slot_hours,   # 🔥 FIXED
        session_type=session_type
    )
    return JsonResponse({"status": "saved"})

from django.http import JsonResponse
def load_timetable(request):

    batch_id = request.GET.get("batch")

    qs = Timetable.objects.select_related("module")

    if batch_id:
        qs = qs.filter(batch_id=batch_id)

    data = []

    for t in qs:
            data.append({
                "module": t.module.id,
                "module_name": t.module.title,
                "week": t.week,
                "day": t.day,
                "slot": t.row_slot,
                "session_type": t.session_type   # 🔥 ADD THIS
            })

    return JsonResponse(data, safe=False)


def load_modules(request, batch_id):

    batch = get_object_or_404(Batch, id=batch_id)

    modules = batch.course.modules.all()

    data = [
        {
            "id": m.id,
            "name": m.code,
            "title": m.title,
            "hours": getattr(m, "total_hours", 0),
        }
        for m in modules
    ]

    return JsonResponse(data, safe=False)

# =========================================================
# 🔷 TIMETABLE CRUD
# =========================================================

class TimetableListView(ListView):
    model = Timetable
    template_name = "timetable/schedule.html"
    context_object_name = "schedules"

    def get_queryset(self):
        return Timetable.objects.select_related(
            "batch", "module"
        ).order_by("date", "start_time")


class TimetableCreateView(CreateView):
    model = Timetable
    fields = ['batch', 'module', 'date', 'start_time', 'end_time']
    template_name = "timetable/add_schedule.html"
    success_url = reverse_lazy('batch:timetable_list')

    def form_valid(self, form):
        form.instance.week = 1
        form.instance.day = 1
        form.instance.row_slot = 1
        return super().form_valid(form)


class TimetableUpdateView(UpdateView):
    model = Timetable
    fields = ['batch', 'module', 'date', 'start_time', 'end_time']
    template_name = "timetable/edit_schedule.html"
    success_url = reverse_lazy('batch:timetable_list')


class TimetableDeleteView(DeleteView):
    model = Timetable
    success_url = reverse_lazy('batch:timetable_list')
