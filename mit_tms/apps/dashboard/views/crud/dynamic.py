from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.urls import (
    reverse_lazy
)

from apps.dashboard.crud_config import (
    CRUD_CONFIG
)


# =========================================================
# BASE DYNAMIC CRUD MIXIN
# =========================================================

class DynamicCRUDMixin:

    model = None
    form_class = None

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        model_name = kwargs.get(
            'model_name'
        )

        config = CRUD_CONFIG.get(
            model_name
        )

        if not config:

            raise ValueError(
                (
                    f'Invalid model: '
                    f'{model_name}'
                )
            )

        self.model = config['model']

        self.form_class = config['form']

        return super().dispatch(
            request,
            *args,
            **kwargs
        )


# =========================================================
# LIST VIEW
# =========================================================

class DynamicListView(
    DynamicCRUDMixin,
    ListView
):

    template_name = (
        "crud/list.html"
    )

    context_object_name = (
        'objects'
    )

    def get_queryset(self):

        return (
            self.model.objects.all()
        )


# =========================================================
# DETAIL VIEW
# =========================================================

class DynamicDetailView(
    DynamicCRUDMixin,
    DetailView
):

    template_name = (
        "crud/detail.html"
    )


# =========================================================
# CREATE VIEW
# =========================================================

class DynamicCreateView(
    DynamicCRUDMixin,
    CreateView
):

    template_name = (
        "crud/form.html"
    )

    def get_success_url(self):

        return reverse_lazy(

            'dashboard:dynamic_list',

            kwargs={
                'model_name':
                    self.kwargs[
                        'model_name'
                    ]
            }
        )


# =========================================================
# UPDATE VIEW
# =========================================================

class DynamicUpdateView(
    DynamicCRUDMixin,
    UpdateView
):

    template_name = (
        "crud/form.html"
    )

    def get_success_url(self):

        return reverse_lazy(

            'dashboard:dynamic_list',

            kwargs={
                'model_name':
                    self.kwargs[
                        'model_name'
                    ]
            }
        )


# =========================================================
# DELETE VIEW
# =========================================================

class DynamicDeleteView(
    DynamicCRUDMixin,
    DeleteView
):

    template_name = (
        "crud/delete.html"
    )

    def get_success_url(self):

        return reverse_lazy(

            'dashboard:dynamic_list',

            kwargs={
                'model_name':
                    self.kwargs[
                        'model_name'
                    ]
            }
        )
