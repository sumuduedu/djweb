from django.shortcuts import render
from .models import Course
# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course


# 📋 List Courses
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"


# 🔍 Course Detail
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_detail.html"


# ➕ Create Course
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'code', 'description', 'duration_hours', 'level']
    template_name = "courses/course_form.html"
    success_url = reverse_lazy('course_list')


# ✏️ Update Course
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'code', 'description', 'duration_hours', 'level']
    template_name = "courses/course_form.html"
    success_url = reverse_lazy('course_list')


# ❌ Delete Course
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"
    success_url = reverse_lazy('course_list')
