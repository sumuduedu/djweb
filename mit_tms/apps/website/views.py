from django.views.generic import TemplateView
from django.contrib import messages

class HomeView(TemplateView):
    template_name = "website/home.html"


class AboutView(TemplateView):
    template_name = "website/about.html"


class ContactView(TemplateView):
    template_name = "website/contact.html"

    def post(self, request, *args, **kwargs):
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # For now just show success message
        messages.success(request, "Message sent successfully!")

        return self.get(request, *args, **kwargs)


from django.views.generic import ListView
from apps.courses.models import Course

class PublicCourseListView(ListView):
    model = Course
    template_name = "website/courses.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(active=True).order_by('-created_at')


# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

@csrf_exempt
def chat_api(request):
    data = json.loads(request.body)
    user_message = data.get("message")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an assistant for MIT Computer Training Center."},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content

    return JsonResponse({"reply": reply})


