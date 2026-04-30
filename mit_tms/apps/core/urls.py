from django.urls import path
from .views import HomeView, dashboard_redirect
from .crud_views import (
    GenericListView,
    GenericCreateView,
    GenericUpdateView,
    GenericDeleteView,
)

app_name = "core"

urlpatterns = [

    # ================= HOME =================
    path('', HomeView.as_view(), name='home'),

    # ================= REDIRECT =================
    path('dashboard/', dashboard_redirect, name='dashboard'),

    # ================= GENERIC CRUD =================
    path('crud/<str:entity>/', GenericListView.as_view(), name='list'),
    path('crud/<str:entity>/create/', GenericCreateView.as_view(), name='create'),
    path('crud/<str:entity>/<int:pk>/edit/', GenericUpdateView.as_view(), name='update'),
    path('crud/<str:entity>/<int:pk>/delete/', GenericDeleteView.as_view(), name='delete'),

]
