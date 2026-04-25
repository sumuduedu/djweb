from django.views.generic import ListView
from apps.courses.models import NCS
from .base import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView




from django.urls import reverse_lazy
from .base import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from apps.courses.models import NCS
from apps.courses.forms.ncs import NCSForm


# ================= LIST =================
class NCSListView(BaseListView):
    model = NCS
    template_name = "ncs/list.html"
    context_object_name = "ncs_list"


# ================= CREATE =================
class NCSCreateView(BaseCreateView):
    model = NCS
    form_class = NCSForm
    template_name = "ncs/form.html"
    success_url = reverse_lazy('courses:ncs_list')

    success_message = "NCS created successfully ✅"
    def form_valid(self, form):
        form.instance.ncs_id = self.kwargs['ncs_id']
        return super().form_valid(form)


# ================= UPDATE =================
class NCSUpdateView(BaseUpdateView):
    model = NCS
    form_class = NCSForm
    template_name = "ncs/form.html"
    success_url = reverse_lazy('courses:ncs_list')

    success_message = "NCS updated successfully ✏️"


# ================= DELETE =================
class NCSDeleteView(BaseDeleteView):
    model = NCS
    template_name = "ncs/confirm_delete.html"
    success_url = reverse_lazy('courses:ncs_list')

    success_message = "NCS deleted successfully ❌"
