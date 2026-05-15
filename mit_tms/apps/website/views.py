from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

import json
from openai import OpenAI

from apps.website.models import (
    ContactMessage,
    MessageReply,
    SentMessage,
)

from apps.courses.models import Course
from apps.enrollment.models import EnrollmentInquiry

from .models import Post, Category

# ==========================================
# 🌐 WEBSITE CONTENT
# ==========================================

from apps.website.sections.home import HOME_HERO,HOME_STATS,HOME_ABOUT,HOME_FEATURES,HOME_COURSES,HOME_TESTIMONIALS
from apps.website.sections.about import ABOUT_HERO
from apps.website.sections.contact import CONTACT_HERO
from apps.website.sections.courses import COURSES_HERO
from apps.website.sections.blog import BLOG_HERO

# ==========================================
# 🤖 OPENAI CLIENT
# ==========================================

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# ==========================================
# 🌐 PUBLIC WEBSITE VIEWS
# ==========================================


class HomeView(TemplateView):

    template_name = "website/pages/home/index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["hero"] = HOME_HERO
        context["home_stats"] = HOME_STATS
        context["home_about"] = HOME_ABOUT
        context["home_features"] = HOME_FEATURES
        context["home_courses"] = HOME_COURSES
        context["home_testimonials"] = HOME_TESTIMONIALS
        return context


class AboutView(TemplateView):

    template_name = "website/pages/about/index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["hero"] = ABOUT_HERO

        return context


class ContactView(TemplateView):

    template_name = "website/pages/contact/index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["hero"] = CONTACT_HERO

        return context

    def post(self, request, *args, **kwargs):

        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )

        messages.success(
            request,
            "✅ Message received successfully!"
        )

        return redirect("contact")


# ==========================================
# 🎓 COURSES
# ==========================================


class PublicCourseListView(ListView):

    model = Course

    template_name = "website/pages/courses/list.html"

    context_object_name = "courses"

    def get_queryset(self):

        return Course.objects.filter(
            status="ACTIVE"
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["hero"] = COURSES_HERO

        return context

class PublicCourseDetailView(DetailView):

    model = Course

    template_name = "website/pages/courses/detail.html"

    context_object_name = "course"

    def get_queryset(self):

        return Course.objects.filter(
            status="ACTIVE"
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["related_courses"] = Course.objects.filter(
            status="ACTIVE"
        ).exclude(
            id=self.object.id
        )[:3]

        return context

# ==========================================
# 📝 PUBLIC BLOG
# ==========================================


class PublicBlogListView(ListView):

    model = Post

    template_name = "website/pages/blog/list.html"

    context_object_name = "posts"

    paginate_by = 6

    def get_queryset(self):

        return Post.objects.filter(
            is_published=True
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["hero"] = BLOG_HERO

        context["recent_posts"] = Post.objects.filter(
            is_published=True
        ).order_by("-created_at")[:5]

        context["categories"] = Category.objects.all()

        return context


class PublicBlogDetailView(DetailView):

    model = Post

    template_name = "website/pages/blog/detail.html"

    context_object_name = "post"

    slug_field = "slug"

    slug_url_kwarg = "slug"

    def get_queryset(self):

        return Post.objects.filter(
            is_published=True
        )

    def get_object(self, queryset=None):

        obj = super().get_object(queryset)

        Post.objects.filter(
            pk=obj.pk
        ).update(views=F("views") + 1)

        obj.refresh_from_db()

        return obj

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["related_posts"] = Post.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(
            id=self.object.id
        )[:3]

        return context


# ==========================================
# 📥 ENROLLMENT
# ==========================================


class EnrollView(TemplateView):

    template_name = "website/pages/enrollment/index.html"

    def post(self, request, *args, **kwargs):

        EnrollmentInquiry.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            course_id=request.POST.get("course"),
            message=request.POST.get("message"),
        )

        messages.success(
            request,
            "✅ Enrollment submitted successfully!"
        )

        return redirect("enroll")


# ==========================================
# 🤖 AI CHAT API
# ==========================================


def chat_api(request):

    data = json.loads(request.body)

    user_message = data.get("message")

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant for "
                        "MIT Computer Training Center."
                    ),
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        reply = response.choices[0].message.content

    except Exception as e:

        print("OPENAI ERROR:", e)

        reply = "⚠️ AI service temporarily unavailable."

    return JsonResponse({"reply": reply})


# ==========================================
# 📥 INBOX
# ==========================================


class InboxView(LoginRequiredMixin, ListView):

    model = ContactMessage

    template_name = "dashboard/mailbox/inbox.html"

    context_object_name = "messages"

    def get_queryset(self):

        return ContactMessage.objects.order_by("-created_at")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["type"] = "inbox"

        return context


# ==========================================
# 📤 SENT MESSAGES
# ==========================================


class SentView(LoginRequiredMixin, ListView):

    model = SentMessage

    template_name = "dashboard/mailbox/sent.html"

    context_object_name = "messages"

    def get_queryset(self):

        return SentMessage.objects.order_by("-sent_at")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["type"] = "sent"

        return context


# ==========================================
# 📩 MESSAGE DETAIL
# ==========================================


class MessageDetailView(LoginRequiredMixin, DetailView):

    model = ContactMessage

    template_name = "dashboard/mailbox/message_detail.html"

    context_object_name = "msg"

    def get_object(self):

        obj = super().get_object()

        if not obj.is_read:

            obj.is_read = True

            obj.save()

        return obj


# ==========================================
# ✉️ REPLY MESSAGE
# ==========================================


class ReplyMessageView(LoginRequiredMixin, View):

    def post(self, request, pk):

        msg = get_object_or_404(
            ContactMessage,
            pk=pk
        )

        reply_text = request.POST.get("reply")

        MessageReply.objects.create(
            message=msg,
            reply_text=reply_text,
        )

        send_mail(
            subject="Re: MIT Inquiry",
            message=reply_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[msg.email],
        )

        messages.success(
            request,
            "Reply sent successfully!"
        )

        return redirect(
            "message_detail",
            pk=pk
        )


# ==========================================
# 🗑 DELETE MESSAGE
# ==========================================


class DeleteMessageView(LoginRequiredMixin, View):

    def post(self, request, pk):

        msg = get_object_or_404(
            ContactMessage,
            pk=pk
        )

        msg.delete()

        messages.success(
            request,
            "Message deleted!"
        )

        return redirect("inbox")


# ==========================================
# ✏️ COMPOSE MESSAGE
# ==========================================


class ComposeMessageView(LoginRequiredMixin, View):

    template_name = "dashboard/mailbox/compose.html"

    def get(self, request):

        return render(
            request,
            self.template_name
        )

    def post(self, request):

        to_email = request.POST.get("email")

        subject = request.POST.get("subject")

        message = request.POST.get("message")

        SentMessage.objects.create(
            to_email=to_email,
            subject=subject,
            message=message,
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
        )

        messages.success(
            request,
            "Email sent successfully!"
        )

        return redirect("sent")


class SentMessageDetailView(LoginRequiredMixin, DetailView):

    model = SentMessage

    template_name = "dashboard/mailbox/sent_detail.html"

    context_object_name = "msg"


# ==========================================
# ✍️ BLOG MANAGEMENT
# ==========================================


class BlogListView(LoginRequiredMixin, ListView):

    model = Post

    template_name = "dashboard/blog/list.html"

    context_object_name = "posts"

    paginate_by = 6

    def get_queryset(self):

        return Post.objects.order_by("-created_at")


class BlogCreateView(LoginRequiredMixin, CreateView):

    model = Post

    template_name = "dashboard/blog/form.html"

    fields = [
        "title",
        "slug",
        "content",
        "category",
        "is_published",
    ]

    def form_valid(self, form):

        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "user_blog_detail",
            kwargs={"slug": self.object.slug}
        )


class BlogUpdateView(LoginRequiredMixin, UpdateView):

    model = Post

    template_name = "dashboard/blog/form.html"

    fields = [
        "title",
        "slug",
        "content",
        "category",
        "is_published",
    ]

    slug_field = "slug"

    slug_url_kwarg = "slug"

    def get_success_url(self):

        return reverse_lazy(
            "user_blog_detail",
            kwargs={"slug": self.object.slug}
        )


class BlogDeleteView(LoginRequiredMixin, DeleteView):

    model = Post

    template_name = "dashboard/blog/confirm_delete.html"

    slug_field = "slug"

    slug_url_kwarg = "slug"

    success_url = reverse_lazy("user_blog_list")

from django.views.generic import TemplateView


class PrivacyPolicyView(TemplateView):
    template_name = 'website/pages/legal/privacy_policy.html'


class TermsOfServiceView(TemplateView):
    template_name = 'website/pages/legal/terms_of_service.html'


class SitemapView(TemplateView):
    template_name = 'website/pages/legal/sitemap.html'
