from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .crud_config import CRUD_CONFIG


class GenericListView(ListView):
    template_name = "crud/list.html"
    context_object_name = "objects"

    def get_config(self):
        return CRUD_CONFIG[self.kwargs["entity"]]

    def get_queryset(self):
        return self.get_config()["model"].objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entity"] = self.kwargs["entity"]
        context["title"] = self.get_config()["name"]
        return context


class GenericCreateView(CreateView):
    template_name = "crud/form.html"

    def get_config(self):
        return CRUD_CONFIG[self.kwargs["entity"]]

    def get_form_class(self):
        return self.get_config()["form"]

    def get_success_url(self):
        return reverse_lazy("core:list", kwargs={"entity": self.kwargs["entity"]})


class GenericUpdateView(UpdateView):
    template_name = "crud/form.html"

    def get_config(self):
        return CRUD_CONFIG[self.kwargs["entity"]]

    def get_queryset(self):
        return self.get_config()["model"].objects.all()

    def get_form_class(self):
        return self.get_config()["form"]

    def get_success_url(self):
        return reverse_lazy("core:list", kwargs={"entity": self.kwargs["entity"]})


class GenericDeleteView(DeleteView):
    template_name = "crud/delete.html"

    def get_config(self):
        return CRUD_CONFIG[self.kwargs["entity"]]

    def get_queryset(self):
        return self.get_config()["model"].objects.all()

    def get_success_url(self):
        return reverse_lazy("core:list", kwargs={"entity": self.kwargs["entity"]})
