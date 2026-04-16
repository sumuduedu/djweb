from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import DetailView
from apps.website.models import ContactMessage, MessageReply, SentMessage
from apps.courses.models import Course

import json
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# ===============================
# 🌐 PUBLIC VIEWS
# ===============================

class HomeView(TemplateView):
    template_name = "website/home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/app/dashboard/')
        return super().dispatch(request, *args, **kwargs)


class AboutView(TemplateView):
    template_name = "website/about.html"


class ContactView(TemplateView):
    template_name = "website/contact.html"

    def post(self, request, *args, **kwargs):
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )

        messages.success(request, "✅ Message received successfully!")
        return redirect('contact')


class PublicCourseListView(ListView):
    model = Course
    template_name = "website/courses.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(active=True).order_by('-created_at')


class PublicCourseDetailView(DetailView):
    model = Course
    template_name = "website/course_detail.html"
    context_object_name = "course"


# ===============================
# 🤖 AI CHAT
# ===============================

def chat_api(request):
    data = json.loads(request.body)
    user_message = data.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an assistant for MIT Computer Training Center."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        print("OPENAI ERROR:", e)
        reply = "⚠️ AI service temporarily unavailable."

    return JsonResponse({"reply": reply})


# ===============================
# 📥 INBOX
# ===============================

class InboxView(LoginRequiredMixin, ListView):
    model = ContactMessage
    template_name = "core/mailbox.html"
    context_object_name = "messages"

    def get_queryset(self):
        return ContactMessage.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'inbox'
        return context


# ===============================
# 📤 SENT
# ===============================

class SentView(LoginRequiredMixin, ListView):
    model = SentMessage
    template_name = "core/mailbox.html"
    context_object_name = "messages"

    def get_queryset(self):
        return SentMessage.objects.order_by('-sent_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'sent'
        return context


# ===============================
# 📩 MESSAGE DETAIL
# ===============================

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = ContactMessage
    template_name = "core/message_detail.html"
    context_object_name = "msg"

    def get_object(self):
        obj = super().get_object()

        if not obj.is_read:
            obj.is_read = True
            obj.save()

        return obj


# ===============================
# ✉️ REPLY MESSAGE
# ===============================

class ReplyMessageView(LoginRequiredMixin, View):

    def post(self, request, pk):
        msg = get_object_or_404(ContactMessage, pk=pk)
        reply_text = request.POST.get("reply")

        MessageReply.objects.create(
            message=msg,
            reply_text=reply_text
        )

        send_mail(
            subject="Re: MIT Inquiry",
            message=reply_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[msg.email],
        )

        messages.success(request, "Reply sent successfully!")
        return redirect('message_detail', pk=pk)


# ===============================
# 🗑 DELETE MESSAGE
# ===============================

class DeleteMessageView(LoginRequiredMixin, View):

    def post(self, request, pk):
        msg = get_object_or_404(ContactMessage, pk=pk)
        msg.delete()

        messages.success(request, "Message deleted!")
        return redirect('inbox')


# ===============================
# ✏️ COMPOSE EMAIL
# ===============================

class ComposeMessageView(LoginRequiredMixin, View):
    template_name = "core/compose.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        to_email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save in DB
        SentMessage.objects.create(
            to_email=to_email,
            subject=subject,
            message=message
        )

        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
        )

        messages.success(request, "Email sent successfully!")
        return redirect('sent')

class SentMessageDetailView(LoginRequiredMixin, DetailView):
    model = SentMessage
    template_name = "core/sent_detail.html"
    context_object_name = "msg"

from apps.enrollment.models import EnrollmentInquiry

class EnrollView(TemplateView):
    template_name = "website/enroll.html"

    def post(self, request, *args, **kwargs):
        EnrollmentInquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            course_id=request.POST.get('course'),
            message=request.POST.get('message')
        )

        messages.success(request, "✅ Enrollment submitted successfully!")
        return redirect('enroll')

from django.views.generic import ListView, DetailView
from django.db.models import F
from .models import Post


class PublicBlogListView(ListView):
    model = Post
    template_name = 'website/blog.html'
    context_object_name = 'posts'
    paginate_by = 6  # optional (adds pagination)

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')


class PublicBlogDetailView(DetailView):
    model = Post
    template_name = 'website/blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # 🔥 Efficient view count increment (no race condition)
        Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)

        # refresh object
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:3]

        return context
