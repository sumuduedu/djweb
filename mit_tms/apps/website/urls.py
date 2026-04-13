from django.urls import path
from .views import HomeView, AboutView, ContactView, PublicCourseListView,EnrollView, chat_api,PublicCourseDetailView

from apps.website.views import (
    InboxView,
    SentView,
    MessageDetailView,
    ReplyMessageView,
    DeleteMessageView,
    ComposeMessageView,
    SentMessageDetailView,

)

urlpatterns = [
    # Public
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('courses/', PublicCourseListView.as_view(), name='public_courses'),

    # Chat
    path('chat/', chat_api, name='chat_api'),

    # Messaging
    path('messages/inbox/', InboxView.as_view(), name='inbox'),
    path('messages/sent/', SentView.as_view(), name='sent'),

    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/reply/', ReplyMessageView.as_view(), name='reply_message'),
    path('messages/<int:pk>/delete/', DeleteMessageView.as_view(), name='delete_message'),
path('messages/sent/<int:pk>/', SentMessageDetailView.as_view(), name='sent_detail'),
    path('compose/', ComposeMessageView.as_view(), name='compose'),
    path('courses/<int:pk>/', PublicCourseDetailView.as_view(), name='course_detail'),
    path('enroll/', EnrollView.as_view(), name='enroll'),
]
