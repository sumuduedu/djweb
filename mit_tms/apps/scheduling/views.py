from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

import json

from apps.batch.models import Batch
from .models import Timetable, TimeSlot
from .forms import TimetableForm
from .utils import generate_timetable


# =========================
# ⚙️ GENERATE TIMETABLE
# =========================

def generate_timetable_view(request, pk):
    batch = get_object_or_404(Batch, pk=pk)

    if batch.timetable.exists():
        messages.warning(request, "Timetable already exists ⚠️")
    else:
        generate_timetable(batch)
        messages.success(request, "Timetable generated successfully ✅")

    return redirect('batch:batch_detail', pk=pk)


# =========================
# 📋 TIMETABLE LIST
# =========================

class TimetableListView(LoginRequiredMixin, ListView):
    model = Timetable
    template_name = "schedule/timetable_list.html"
    context_object_name = "timetables"
    ordering = ["-date"]


# =========================
# ➕ CREATE
# =========================

class TimetableCreateView(LoginRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = "schedule/timetable_form.html"
    success_url = reverse_lazy("schedule:list")


# =========================
# ✏️ UPDATE
# =========================

class TimetableUpdateView(LoginRequiredMixin, UpdateView):
    model = Timetable
    form_class = TimetableForm
    template_name = "schedule/timetable_form.html"
    success_url = reverse_lazy("schedule:list")


# =========================
# ❌ DELETE
# =========================

class TimetableDeleteView(LoginRequiredMixin, DeleteView):
    model = Timetable
    template_name = "schedule/timetable_confirm_delete.html"
    success_url = reverse_lazy("schedule:list")


# =========================
# 📅 CALENDAR VIEW
# =========================

class TimetableCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "schedule/timetable_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["batches"] = Batch.objects.all()
        context["slots"] = TimeSlot.objects.all()
        return context


# =========================
# 🔥 API (SAVE EVENT)
# =========================

@csrf_exempt
def save_calendar_event(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)

        Timetable.objects.create(
            batch_id=data.get("batch"),
            module_id=data.get("module"),
            date=data.get("date"),
            slot_id=data.get("slot"),
            session_type=data.get("session_type"),
        )

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from django.views.generic import DetailView
from apps.scheduling.models import ModulePlan
from apps.batch.models import Batch


class GanttChartView(DetailView):
    model = Batch
    template_name = "batch/gantt.html"
    context_object_name = "batch"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        batch = self.get_object()

        # 🔥 get module plans (your schedule)
        plans = ModulePlan.objects.filter(batch=batch).select_related('module')

        context['plans'] = plans

        return context


from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import ModulePlan
from .forms import ModulePlanForm
from apps.batch.models import Batch


class ModulePlanCreateView(LoginRequiredMixin, CreateView):
    model = ModulePlan
    form_class = ModulePlanForm
    template_name = "schedule/module_plan_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(Batch, pk=kwargs['batch_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['batch'] = self.batch   # 🔥 IMPORTANT
        return kwargs

    def form_valid(self, form):
        form.instance.batch = self.batch
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('batch:batch_detail', args=[self.batch.pk])
