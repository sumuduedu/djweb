from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.crud_config import CRUD_CONFIG


class DynamicListView(ListView):

    template_name = "crud/list.html"

    def get_queryset(self):
        entity = self.kwargs['entity']
        return CRUD_CONFIG[entity]['model'].objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entity = self.kwargs['entity']
        model = CRUD_CONFIG[entity]['model']

        context['entity'] = entity
        context['title'] = CRUD_CONFIG[entity]['name']

        # fields (exclude id if you want)
        fields = [field.name for field in model._meta.fields]
        context['fields'] = fields

        # ✅ build rows (NO template filter needed)
        context['rows'] = [
    {
        "obj": obj,
        "values": [getattr(obj, field, "") for field in fields]
    }

    for obj in context['object_list']
]

        return context


class DynamicCreateView(CreateView):

    def get_form_class(self):
        entity = self.kwargs['entity']
        return CRUD_CONFIG[entity]['form']

    def get_success_url(self):
        return reverse_lazy('core:dynamic_list', kwargs={
            'entity': self.kwargs['entity']
        })

    def get_template_names(self):
        return ["crud/form.html"]


class DynamicUpdateView(UpdateView):

    def get_queryset(self):
        entity = self.kwargs['entity']
        return CRUD_CONFIG[entity]['model'].objects.all()

    def get_form_class(self):
        entity = self.kwargs['entity']
        return CRUD_CONFIG[entity]['form']

    def get_success_url(self):
        return reverse_lazy('core:dynamic_list', kwargs={
            'entity': self.kwargs['entity']
        })

    def get_template_names(self):
        return ["crud/form.html"]


class DynamicDeleteView(DeleteView):

    def get_queryset(self):
        entity = self.kwargs['entity']
        return CRUD_CONFIG[entity]['model'].objects.all()

    def get_success_url(self):
        return reverse_lazy('core:dynamic_list', kwargs={
            'entity': self.kwargs['entity']
        })

    def get_template_names(self):
        return ["crud/delete.html"]
