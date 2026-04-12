from django.urls import path
from .views import HomeView, AboutView, ContactView, PublicCourseListView, chat_api

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('courses/', PublicCourseListView.as_view(), name='public_courses'),

    # Chat API
    path('chat/', chat_api, name='chat_api'),
]
