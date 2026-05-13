from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.forms import modelformset_factory
from django.db import transaction

from apps.core.permission_engine import PermissionEngine

from .base import BaseListView, BaseUpdateView, BaseDeleteView
from apps.courses.views.dynbase import DynamicCreateView
from .base import BaseDetailView

from ..models import Course, LearningResource
from ..forms import CourseForm
from ..services.course_service import CourseService
from apps.courses.selectors.course_selector import CourseSelector
from ..config.form_layout import COURSE_FORM_LAYOUT, RELATION_LAYOUT


# =========================
# 🔷 COURSE LIST
# =========================
class CourseListView(BaseListView):
    template_name = "courses/course_lists.html"

    def dispatch(self, request, *args, **kwargs):
        if not PermissionEngine.can(request.user, "course", "read"):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # ⚠️ IMPORTANT: do NOT use invalid prefetch like "resources"
        return CourseSelector.list(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["table"] = CourseService.get_table(self.request.user)

        context["can_create"] = PermissionEngine.can(self.request.user, "course", "create")
        context["can_update"] = PermissionEngine.can(self.request.user, "course", "update")
        context["can_delete"] = PermissionEngine.can(self.request.user, "course", "delete")

        return context


# =========================
# 🔷 COURSE DETAIL
# =========================
class CourseDetailView(BaseDetailView):
    model = Course
    template_name = "courses/course_detail.html"

    def get_extra_context(self):
        course = self.object

        # safe related access (requires related_name="modules")
        modules = course.modules.all()

        total_theory = sum(m.theory_hours or 0 for m in modules)
        total_practical = sum(m.practical_hours or 0 for m in modules)

        course_theory = course.theory_hours or 0
        course_practical = course.practical_hours or 0
        course_assignment = course.assignment_hours or 0

        return {
            "total_theory": total_theory,
            "total_practical": total_practical,
            "total_hours_sum": total_theory + total_practical,
            "total_months": course.duration_months,

            "course_theory": course_theory,
            "course_practical": course_practical,
            "course_assignment": course_assignment,  # ✅ FIXED

            "course_level": course.level,
            "course_medium": course.medium,
            "delivery_mode": course.delivery_mode,
            "course_mode": course.course_mode,
            "entry_qualification": course.entry_qualification,

            "nvq_level": course.nvq_level,
            "qualification_code": course.qualification_code,

            "batches_per_year": course.batches_per_year,
            "students_per_batch": course.students_per_batch,

            "course_fee": course.course_fee,
            "is_free": course.is_free,
            "fee_includes": course.fee_includes,

            "tools": course.tools_available,
            "equipment": course.equipment_available,
            "machinery": course.machinery_available,

            "prerequisite": course.prerequisite,
            "learning_outcomes": course.learning_outcomes,

            "industry": course.industry,
            "equivalent_course": course.equivalent_course,

            "is_matching": (
                total_theory == course_theory and
                total_practical == course_practical
            )
        }


# =========================
# 🔷 COURSE CREATE
# =========================
class CourseCreateView(DynamicCreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")

    form_layout = COURSE_FORM_LAYOUT
    relation_layout = RELATION_LAYOUT

    relation_models = {
        "learning_resources": LearningResource
    }

    parent_field = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        relation_formsets = {}

        for rel in self.relation_layout:
            model = self.relation_models.get(rel["name"])
            if not model:
                continue

            FormSet = modelformset_factory(
                model,
                fields=rel["fields"],
                extra=1,
                can_delete=True
            )

            prefix = rel["name"]

            if self.request.POST:
                relation_formsets[rel["name"]] = FormSet(
                    self.request.POST,
                    self.request.FILES,
                    queryset=model.objects.none(),
                    prefix=prefix
                )
            else:
                relation_formsets[rel["name"]] = FormSet(
                    queryset=model.objects.none(),
                    prefix=prefix
                )

        context["relation_formsets"] = relation_formsets

        context["relation_items"] = [
            {
                "name": rel["name"],
                "formset": relation_formsets.get(rel["name"]),
                "label": rel.get("label", rel["name"].title())
            }
            for rel in self.relation_layout
        ]

        context["form_layout"] = self.form_layout

        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        relation_formsets = context.get("relation_formsets", {})

        for formset in relation_formsets.values():
            if not formset.is_valid():
                return self.form_invalid(form)

        self.object = form.save()

        for formset in relation_formsets.values():
            instances = formset.save(commit=False)

            for obj in instances:
                setattr(obj, self.parent_field, self.object)
                obj.save()

            for obj in formset.deleted_objects:
                obj.delete()

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


# =========================
# 🔷 COURSE UPDATE
# =========================
class CourseUpdateView(BaseUpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")

    success_message = "Course updated successfully ✏️"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form_layout"] = COURSE_FORM_LAYOUT
        context["relation_layout"] = RELATION_LAYOUT

        relation_formsets = {}

        for rel in RELATION_LAYOUT:
            model = LearningResource

            FormSet = modelformset_factory(
                model,
                fields=rel["fields"],
                extra=1,
                can_delete=True
            )

            prefix = rel["name"]

            if self.request.POST:
                relation_formsets[rel["name"]] = FormSet(
                    self.request.POST,
                    self.request.FILES,
                    queryset=model.objects.filter(course=self.object),
                    prefix=prefix
                )
            else:
                relation_formsets[rel["name"]] = FormSet(
                    queryset=model.objects.filter(course=self.object),
                    prefix=prefix
                )

        context["relation_formsets"] = relation_formsets

        return context


# =========================
# 🔷 COURSE DELETE
# =========================
class CourseDeleteView(BaseDeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"
    success_url = reverse_lazy("courses:course_list")

    success_message = "Course deleted successfully ❌"
