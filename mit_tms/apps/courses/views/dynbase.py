from django.forms import modelformset_factory
from .base import *


class DynamicListView(BaseListView):
    table_service = None
    permission_entity = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["table"] = self.table_service(self.request.user)

        context["can_create"] = PermissionEngine.can(self.request.user, self.permission_entity, "create")
        context["can_update"] = PermissionEngine.can(self.request.user, self.permission_entity, "update")
        context["can_delete"] = PermissionEngine.can(self.request.user, self.permission_entity, "delete")

        return context
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .base import BaseCreateView
from django.forms import inlineformset_factory

class DynamicCreateView(BaseCreateView):

    form_layout = None
    relation_layout = None
    relation_models = {}
    parent_field = None   # 🔥 IMPORTANT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form_layout"] = self.form_layout
        context["relation_layout"] = self.relation_layout

        relation_formsets = {}

        for rel in self.relation_layout:

            model = self.relation_models.get(rel["name"])
            if not model:
                continue


            FormSet = inlineformset_factory(
                self.model,   # 🔥 Parent (Course)
                model,        # 🔥 Child (LearningResource)
                fields=rel["fields"],
                extra=1,
                can_delete=True
            )

            prefix = rel["name"]

            if self.request.POST:
                formset = FormSet(
                    self.request.POST,
                    self.request.FILES,
                    queryset=model.objects.none(),
                    prefix=prefix
                )
            else:
                formset = FormSet(
                    queryset=model.objects.none(),
                    prefix=prefix
                )

            relation_formsets[rel["name"]] = formset

        context["relation_formsets"] = relation_formsets
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        relation_formsets = context["relation_formsets"]

        # 🔥 Validate ALL formsets first
        for formset in relation_formsets.values():
            if not formset.is_valid():
                return self.form_invalid(form)

        # 🔥 Save main object
        self.object = form.save()

        # 🔥 Save relations
        for name, formset in relation_formsets.items():

            instances = formset.save(commit=False)

            for obj in instances:
                setattr(obj, self.parent_field, self.object)  # 🔥 dynamic
                obj.save()

            # 🔥 handle delete (important)
            for obj in formset.deleted_objects:
                obj.delete()

        return super().form_valid(form)

class DynamicUpdateView(BaseUpdateView):
    form_layout = None
    relation_layout = None
    relation_models = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form_layout"] = self.form_layout
        context["relation_layout"] = self.relation_layout

        relation_formsets = {}

        for rel in self.relation_layout:

            model = self.relation_models.get(rel["name"])
            if not model:
                continue

            FormSet = modelformset_factory(
                model,
                fields=rel["fields"],
                extra=0,
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

    def form_valid(self, form):
        context = self.get_context_data()
        relation_formsets = context["relation_formsets"]

        self.object = form.save()

        for name, formset in relation_formsets.items():
            if formset.is_valid():

                instances = formset.save(commit=False)

                for obj in instances:
                    obj.course = self.object
                    obj.save()

                for obj in formset.deleted_objects:
                    obj.delete()

        return super().form_valid(form)
