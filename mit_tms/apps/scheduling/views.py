from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import timedelta

from .models import Batch, Timetable, TimeSlot
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
    template_name = "batch/timetable_list.html"


# =========================
# ➕ CREATE
# =========================

class TimetableCreateView(LoginRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = "batch/timetable_form.html"
    success_url = reverse_lazy("batch:timetable_list")


# =========================
# ✏️ UPDATE
# =========================

class TimetableUpdateView(LoginRequiredMixin, UpdateView):
    model = Timetable
    form_class = TimetableForm
    template_name = "batch/timetable_form.html"
    success_url = reverse_lazy("batch:timetable_list")


# =========================
# ❌ DELETE
# =========================

class TimetableDeleteView(LoginRequiredMixin, DeleteView):
    model = Timetable
    template_name = "batch/timetable_confirm_delete.html"
    success_url = reverse_lazy("batch:timetable_list")


# =========================
# 📅 CALENDAR VIEW
# =========================

class TimetableCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "batch/timetable_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["batches"] = Batch.objects.all()
        context["slots"] = TimeSlot.objects.all()
        return context


# =========================
# 🔥 API (SAVE)
# =========================

@csrf_exempt
def save_calendar_event(request):
    data = json.loads(request.body)

    Timetable.objects.create(
        batch_id=data["batch"],
        module_id=data["module"],
        date=data["date"],
        slot_id=data["slot"],
        session_type=data["session_type"]
    )

    return JsonResponse({"success": True})
