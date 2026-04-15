from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .services import enroll_student


@login_required
def enroll_view(request, batch_id):
    enroll_student(request.user, batch_id)
    return redirect("student_dashboard")


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def apply_student(request, course_id):
    return redirect('core:student_dashboard')

@login_required
def apply_teacher(request, course_id):
    return redirect('core:teacher_dashboard')

@login_required
def apply_parent(request, course_id):
    return redirect('core:parent_dashboard')
