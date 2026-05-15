from django.urls import path

from apps.dashboard.views.crud.dynamic import (

    DynamicListView,
    DynamicCreateView,
    DynamicUpdateView,
    DynamicDeleteView,
    DynamicDetailView,
)


urlpatterns = [

    path(
        '<str:model_name>/',
        DynamicListView.as_view(),
        name='dynamic_list'
    ),

    path(
        '<str:model_name>/create/',
        DynamicCreateView.as_view(),
        name='dynamic_create'
    ),

    path(
        '<str:model_name>/<int:pk>/',
        DynamicDetailView.as_view(),
        name='dynamic_detail'
    ),

    path(
        '<str:model_name>/<int:pk>/edit/',
        DynamicUpdateView.as_view(),
        name='dynamic_update'
    ),

    path(
        '<str:model_name>/<int:pk>/delete/',
        DynamicDeleteView.as_view(),
        name='dynamic_delete'
    ),
]
