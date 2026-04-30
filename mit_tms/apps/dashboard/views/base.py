from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from apps.accounts.models import Profile

class BaseView(LoginRequiredMixin, TemplateView):
    allowed_roles = None

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        self.profile = getattr(user, "profile", None)

        if not self.profile:
            raise PermissionDenied("Profile missing")

        # Always define role
        self.role = (self.profile.role or "GUEST").upper()

        # Superuser bypass
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Role restriction
        if self.allowed_roles:
            allowed = [r.upper() for r in self.allowed_roles]

            if self.role not in allowed:
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def has_role(self, *roles):
        return self.role in [r.upper() for r in roles]

    def is_student(self):
        return self.role == "STUDENT"

    def is_teacher(self):
        return self.role == "TEACHER"

    def is_admin(self):
        return self.role == "ADMIN" or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "profile": self.profile,
            "role": self.role,
            "is_admin": self.is_admin(),
            "is_staff": self.has_role("STAFF"),
            "is_teacher": self.is_teacher(),
            "is_student": self.is_student(),
            "is_parent": self.has_role("PARENT"),
            "is_guest": self.has_role("GUEST"),
        })

        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages


# =====================================
# 🔷 BASE LIST VIEW
# =====================================
class BaseListView(LoginRequiredMixin, ListView):
    paginate_by = 10


# =====================================
# 🔷 BASE CREATE VIEW
# =====================================
class BaseCreateView(LoginRequiredMixin, CreateView):
    success_message = "Created successfully ✅"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "object"

    def get_extra_context(self):
        """
        Override this in child classes to add extra context
        """
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        extra = self.get_extra_context()
        if extra:
            context.update(extra)

        return context
# =====================================
# 🔷 BASE UPDATE VIEW
# =====================================
class BaseUpdateView(LoginRequiredMixin, UpdateView):
    success_message = "Updated successfully ✏️"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


# =====================================
# 🔷 BASE DELETE VIEW
# =====================================
class BaseDeleteView(LoginRequiredMixin, DeleteView):
    success_message = "Deleted successfully ❌"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# =====================================
# 🔥 CHILD BASE LIST VIEW
# =====================================
class BaseChildListView(BaseListView):
    parent_field = None           # e.g. "task"
    parent_url_kwarg = None       # e.g. "task_id"

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.parent_field and self.parent_url_kwarg:
            return queryset.filter(
                **{f"{self.parent_field}_id": self.kwargs[self.parent_url_kwarg]}
            )

        return queryset


# =====================================
# 🔥 CHILD BASE CREATE VIEW
# =====================================
class BaseChildCreateView(BaseCreateView):
    parent_field = None
    parent_url_kwarg = None

    def form_valid(self, form):
        if self.parent_field and self.parent_url_kwarg:
            setattr(
                form.instance,
                f"{self.parent_field}_id",
                self.kwargs[self.parent_url_kwarg]
            )
        return super().form_valid(form)



from django.shortcuts import get_object_or_404


class BaseChildDetailView(BaseDetailView):
    parent_field = None
    parent_url_kwarg = None

    def get_object(self, queryset=None):
        queryset = self.get_queryset()

        if self.parent_field and self.parent_url_kwarg:
            filter_kwargs = {
                "pk": self.kwargs.get("pk"),
                f"{self.parent_field}_id": self.kwargs.get(self.parent_url_kwarg)
            }
            return get_object_or_404(queryset, **filter_kwargs)

        return super().get_object(queryset)


# =====================================
# 🔥 CHILD BASE UPDATE VIEW
# =====================================
class BaseChildUpdateView(BaseUpdateView):
    parent_field = None
    parent_url_kwarg = None

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.parent_field and self.parent_url_kwarg:
            return queryset.filter(
                **{f"{self.parent_field}_id": self.kwargs[self.parent_url_kwarg]}
            )

        return queryset


# =====================================
# 🔥 CHILD BASE DELETE VIEW
# =====================================
class BaseChildDeleteView(BaseDeleteView):
    parent_field = None
    parent_url_kwarg = None

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.parent_field and self.parent_url_kwarg:
            return queryset.filter(
                **{f"{self.parent_field}_id": self.kwargs[self.parent_url_kwarg]}
            )

        return queryset
