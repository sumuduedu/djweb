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


from datetime import datetime

def parse_time(t):
    if not t:
        return None

    t = t.strip().lower()

    t = t.replace("a.m.", "AM").replace("p.m.", "PM")
    t = t.replace("am", "AM").replace("pm", "PM")

    try:
        return datetime.strptime(t, "%H:%M")
    except:
        try:
            return datetime.strptime(t, "%I:%M %p")
        except:
            return None

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
from datetime import timedelta
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Batch, TimeSlot

class GanttView(View):

    def get(self, request):

        batch_id = request.GET.get("batch")
        week = int(request.GET.get("week", 1))   # ✅ GET WEEK

        batch = get_object_or_404(Batch, id=batch_id)

        # 🔥 BASE DATE
        base_date = batch.start_date

        # 🔥 APPLY WEEK OFFSET
        start_of_week = base_date + timedelta(days=(week - 1) * 7)

        # 🔥 GENERATE DAYS
        days = []
        for i in range(7):
            days.append(start_of_week + timedelta(days=i))

        return render(request, "batch/gantt.html", {
            "batch": batch,
            "modules": batch.course.modules.all(),
            "slots": TimeSlot.objects.all().order_by("order"),
            "days": days,
            "current_week": week   # ✅ IMPORTANT
        })


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


from django.http import JsonResponse
from apps.courses.models import Module

def load_modules_by_batch(request):
    batch_id = request.GET.get("batch_id")

    if not batch_id:
        return JsonResponse([], safe=False)

    modules = Module.objects.filter(
        course__batches__id=batch_id
    ).values("id", "title")

    return JsonResponse(list(modules), safe=False)
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta

from .models import Timetable, Batch


@csrf_exempt
def save_timetable(request):

    data = json.loads(request.body)

    batch = get_object_or_404(Batch, id=data["batch"])

    week = int(data["week"])
    day = int(data["day"])
    slot_id = int(data["slot"])

    # =========================
    # DATE CALC (FIRST FIX)
    # =========================
    total_days = (week - 1) * batch.days_per_week + (day - 1)
    class_date = batch.start_date + timedelta(days=total_days)

    # =========================
    # DELETE
    # =========================
    if data.get("delete"):
        Timetable.objects.filter(
            batch=batch,
            week=week,
            day=day,
            slot_id=slot_id,
            module_id=data.get("module")
        ).delete()

        return JsonResponse({"status": "deleted"})

    # =========================
    # CONFLICT CHECK (FIXED POSITION)
    # =========================
    conflict = Timetable.objects.filter(
        date=class_date,
        slot_id=slot_id
    ).exclude(batch=batch).exists()

    if conflict:
        return JsonResponse({
            "status": "conflict",
            "message": "Another batch already has a class at this time"
        }, status=409)

    # =========================
    # REMOVE OLD (SAME SLOT)
    # =========================
    Timetable.objects.filter(
        batch=batch,
        week=week,
        day=day,
        slot_id=slot_id
    ).delete()

    # =========================
    # TIME CALC
    # =========================
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    start = parse_time(start_time)
    end = parse_time(end_time)

    if start and end:
        slot_hours = (end - start).seconds / 3600
    else:
        slot_hours = 1

    # =========================
    # SESSION TYPE
    # =========================
    session_type = data.get("session_type", "THEORY")

    # =========================
    # CREATE
    # =========================
    Timetable.objects.create(
        batch=batch,
        module_id=data["module"],
        week=week,
        day=day,
        slot_id=slot_id,
        date=class_date,
        hours=slot_hours,
        session_type=session_type
    )

    return JsonResponse({"status": "saved"})
def load_timetable(request):

    batch_id = request.GET.get("batch")

    qs = Timetable.objects.select_related("module", "slot")

    if batch_id:
        qs = qs.filter(batch_id=batch_id)

    data = []

    for t in qs:
        data.append({
            "module": t.module.id,
            "module_name": t.module.title,
            "week": t.week,
            "day": t.day,
            "slot": t.slot.id,
            "session_type": t.session_type
        })

    return JsonResponse(data, safe=False)


# =========================================================
# 🔷 TIMETABLE CRUD
# =========================================================
# =========================================================
# 🔷 TIMETABLE CRUD (CLEAN FINAL)
# =========================================================
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger

from django.db.models import Count, Q
from django.core.paginator import EmptyPage, PageNotAnInteger
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


from datetime import datetime

def parse_time(t):
    if not t:
        return None

    t = t.strip().lower()

    t = t.replace("a.m.", "AM").replace("p.m.", "PM")
    t = t.replace("am", "AM").replace("pm", "PM")

    try:
        return datetime.strptime(t, "%H:%M")
    except:
        try:
            return datetime.strptime(t, "%I:%M %p")
        except:
            return None

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
from datetime import timedelta
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Batch, TimeSlot

class GanttView(View):

    def get(self, request):

        batch_id = request.GET.get("batch")
        week = int(request.GET.get("week", 1))   # ✅ GET WEEK

        batch = get_object_or_404(Batch, id=batch_id)

        # 🔥 BASE DATE
        base_date = batch.start_date

        # 🔥 APPLY WEEK OFFSET
        start_of_week = base_date + timedelta(days=(week - 1) * 7)

        # 🔥 GENERATE DAYS
        days = []
        for i in range(7):
            days.append(start_of_week + timedelta(days=i))

        return render(request, "batch/gantt.html", {
            "batch": batch,
            "modules": batch.course.modules.all(),
            "slots": TimeSlot.objects.all().order_by("order"),
            "days": days,
            "current_week": week   # ✅ IMPORTANT
        })


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
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta

from .models import Timetable, Batch


@csrf_exempt
def save_timetable(request):

    data = json.loads(request.body)

    batch = get_object_or_404(Batch, id=data["batch"])

    week = int(data["week"])
    day = int(data["day"])
    slot_id = int(data["slot"])

    # =========================
    # DATE CALC (FIRST FIX)
    # =========================
    total_days = (week - 1) * batch.days_per_week + (day - 1)
    class_date = batch.start_date + timedelta(days=total_days)

    # =========================
    # DELETE
    # =========================
    if data.get("delete"):
        Timetable.objects.filter(
            batch=batch,
            week=week,
            day=day,
            slot_id=slot_id,
            module_id=data.get("module")
        ).delete()

        return JsonResponse({"status": "deleted"})

    # =========================
    # CONFLICT CHECK (FIXED POSITION)
    # =========================
    conflict = Timetable.objects.filter(
        date=class_date,
        slot_id=slot_id
    ).exclude(batch=batch).exists()

    if conflict:
        return JsonResponse({
            "status": "conflict",
            "message": "Another batch already has a class at this time"
        }, status=409)

    # =========================
    # REMOVE OLD (SAME SLOT)
    # =========================
    Timetable.objects.filter(
        batch=batch,
        week=week,
        day=day,
        slot_id=slot_id
    ).delete()

    # =========================
    # TIME CALC
    # =========================
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    start = parse_time(start_time)
    end = parse_time(end_time)

    if start and end:
        slot_hours = (end - start).seconds / 3600
    else:
        slot_hours = 1

    # =========================
    # SESSION TYPE
    # =========================
    session_type = data.get("session_type", "THEORY")

    # =========================
    # CREATE
    # =========================
    Timetable.objects.create(
        batch=batch,
        module_id=data["module"],
        week=week,
        day=day,
        slot_id=slot_id,
        date=class_date,
        hours=slot_hours,
        session_type=session_type
    )

    return JsonResponse({"status": "saved"})
def load_timetable(request):

    batch_id = request.GET.get("batch")

    qs = Timetable.objects.select_related("module", "slot")

    if batch_id:
        qs = qs.filter(batch_id=batch_id)

    data = []

    for t in qs:
        data.append({
            "module": t.module.id,
            "module_name": t.module.title,
            "week": t.week,
            "day": t.day,
            "slot": t.slot.id,
            "session_type": t.session_type
        })

    return JsonResponse(data, safe=False)


# =========================================================
# 🔷 TIMETABLE CRUD
# =========================================================
# =========================================================
# 🔷 TIMETABLE CRUD (CLEAN FINAL)
# =========================================================
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger

from django.db.models import Count, Q
from django.core.paginator import EmptyPage, PageNotAnInteger

class TimetableListView(LoginRequiredMixin, ListView):
    model = Timetable
    template_name = "batch/timetable_list.html"
    context_object_name = "object_list"
    paginate_by = 10

    def get_queryset(self):
        qs = Timetable.objects.select_related(
            "batch", "module", "slot", "batch__course"
        )

        batch = self.request.GET.get("batch")
        week = self.request.GET.get("week")
        search = self.request.GET.get("search")

        if batch:
            qs = qs.filter(batch_id=batch)

        if week:
            qs = qs.filter(week=week)

        if search:
            qs = qs.filter(
                Q(module__title__icontains=search) |
                Q(batch__name__icontains=search)
            )

        return qs.order_by("date", "slot__start_time")

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(queryset, page_size)
        page = self.request.GET.get("page")

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return paginator, page_obj, page_obj.object_list, page_obj.has_other_pages()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booked_dates = Timetable.objects.values_list("date", flat=True).distinct()


        conflicts = (
            Timetable.objects.values("batch", "date", "slot")
            .annotate(total=Count("id"))
            .filter(total__gt=1)
        )

        context["conflict_set"] = {
            f"{c['batch']}-{c['date']}-{c['slot']}"
            for c in conflicts
        }
        context["booked_dates"] = list(booked_dates)
        context["batches"] = Batch.objects.all()
        context["selected_batch"] = self.request.GET.get("batch", "")
        context["selected_week"] = self.request.GET.get("week", "")
        context["search_query"] = self.request.GET.get("search", "")

        return context
from .forms import TimetableForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect

class TimetableCreateView(LoginRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = "batch/timetable_form.html"
    success_url = reverse_lazy("batch:timetable_list")

    def form_valid(self, form):
        batch = form.cleaned_data["batch"]
        date = form.cleaned_data["date"]
        slot = form.cleaned_data["slot"]

        # 🔥 CHECK CONFLICT BEFORE SAVE
        if Timetable.objects.filter(batch=batch, date=date, slot=slot).exists():
            form.add_error(None, "⚠️ Conflict: This batch already has a session in this time slot.")
            return self.form_invalid(form)

        return super().form_valid(form)

class TimetableUpdateView(LoginRequiredMixin, UpdateView):
    model = Timetable
    form_class = TimetableForm
    template_name = "batch/timetable_form.html"
    success_url = reverse_lazy("batch:timetable_list")

    def form_valid(self, form):
        batch = form.cleaned_data["batch"]
        date = form.cleaned_data["date"]
        slot = form.cleaned_data["slot"]

        # 🔥 EXCLUDE CURRENT OBJECT
        if Timetable.objects.filter(
            batch=batch,
            date=date,
            slot=slot
        ).exclude(pk=self.object.pk).exists():
            form.add_error(None, "⚠️ Conflict: This slot is already taken.")
            return self.form_invalid(form)

        return super().form_valid(form)

class TimetableDeleteView(LoginRequiredMixin, DeleteView):
    model = Timetable
    template_name = "batch/timetable_confirm_delete.html"
    success_url = reverse_lazy("batch:timetable_list")

from django.views.generic import DetailView

class TimetableDetailView(LoginRequiredMixin, DetailView):
    model = Timetable
    template_name = "batch/timetable_detail.html"


from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect

class TimetableCreateView(LoginRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = "batch/timetable_form.html"
    success_url = reverse_lazy("batch:timetable_list")

    def form_valid(self, form):
        # 🔥 DEBUG (optional)
        if not form.cleaned_data.get("date"):
            form.add_error("date", "Date is required.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM ERRORS:", form.errors)  # 🔥 debug
        return super().form_invalid(form)

class TimetableUpdateView(LoginRequiredMixin, UpdateView):
    model = Timetable
    fields = ["batch", "module", "date", "slot", "session_type"]
    template_name = "batch/timetable_form.html"
    success_url = reverse_lazy("batch:timetable_list")

    def form_valid(self, form):

        batch = form.cleaned_data["batch"]
        date = form.cleaned_data["date"]
        slot = form.cleaned_data["slot"]

        exists = Timetable.objects.filter(
            batch=batch,
            date=date,
            slot=slot
        ).exclude(pk=self.object.pk).exists()

        if exists:
            form.add_error(None, "⚠️ Conflict detected")
            return self.form_invalid(form)

        return super().form_valid(form)


class TimetableDeleteView(LoginRequiredMixin, DeleteView):
    model = Timetable
    template_name = "batch/timetable_confirm_delete.html"
    success_url = reverse_lazy("batch:timetable_list")

from django.views.generic import DetailView

class TimetableDetailView(LoginRequiredMixin, DetailView):
    model = Timetable
    template_name = "batch/timetable_detail.html"

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Batch, TimeSlot

class TimetableCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "batch/timetable_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["batches"] = Batch.objects.select_related("course").order_by("name")
        context["slots"] = TimeSlot.objects.order_by("order")

        return context

@csrf_exempt
def save_calendar_event(request):
    if request.method == "POST":
        data = json.loads(request.body)

        batch_id = data.get("batch")
        module_id = data.get("module")
        date = data.get("date")
        slot_id = data.get("slot")
        session_type = data.get("session_type")

        # 🔥 Conflict check
        if Timetable.objects.filter(batch_id=batch_id, date=date, slot_id=slot_id).exists():
            return JsonResponse({"error": "Conflict!"}, status=400)

        Timetable.objects.create(
            batch_id=batch_id,
            module_id=module_id,
            date=date,
            slot_id=slot_id,
            session_type=session_type
        )

        return JsonResponse({"success": True})

from django.http import JsonResponse

def get_timetable_by_date(request):
    date = request.GET.get("date")

    timetable = Timetable.objects.filter(date=date).select_related(
        "batch", "module", "slot"
    ).first()

    if not timetable:
        return JsonResponse({"exists": False})

    return JsonResponse({
        "exists": True,
        "batch": timetable.batch.id,
        "module": timetable.module.id,
        "slot": timetable.slot.id,
        "session_type": timetable.session_type,
    })


@csrf_exempt
def update_event_date(request):
    if request.method == "POST":
        data = json.loads(request.body)

        event_id = data.get("id")
        new_date = data.get("date")

        try:
            t = Timetable.objects.get(id=event_id)
            t.date = new_date
            t.save()

            return JsonResponse({"success": True})
        except:
            return JsonResponse({"error": "Not found"}, status=404)


class WeeklyTimetableView(TemplateView):
    template_name = "batch/weekly.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["slots"] = TimeSlot.objects.order_by("order")
        context["days"] = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

        context["data"] = Timetable.objects.select_related("module")

        return context

from django.http import JsonResponse
from .models import Timetable

def load_events(request):
    events = []

    for t in Timetable.objects.select_related("module"):
        events.append({
            "id": t.id,
            "title": f"{t.module.title} ({t.session_type})",
            "start": t.date.isoformat(),
            "color": "#3b82f6" if t.session_type == "THEORY" else "#22c55e",
        })

    return JsonResponse(events, safe=False)

@csrf_exempt
def create_event(request):
    data = json.loads(request.body)

    t = Timetable.objects.create(
        batch_id=data["batch"],
        module_id=data["module"],
        date=data["date"],
        slot_id=data["slot"],
        session_type=data["session_type"]
    )

    return JsonResponse({"id": t.id})

@csrf_exempt
def update_event(request):
    data = json.loads(request.body)

    t = Timetable.objects.get(id=data["id"])
    t.date = data["date"]
    t.save()

    return JsonResponse({"success": True})

@csrf_exempt
def delete_event(request):
    data = json.loads(request.body)

    Timetable.objects.filter(id=data["id"]).delete()

    return JsonResponse({"success": True})

@csrf_exempt
def clear_timetable(request):
    if request.method == "POST":
        data = json.loads(request.body)

        batch = data.get("batch")

        Timetable.objects.filter(batch_id=batch).delete()

        return JsonResponse({"success": True})
