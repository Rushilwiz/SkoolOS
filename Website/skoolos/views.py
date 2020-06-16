from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from api.models import Student, Teacher, Class, Assignment

# Create your views here.

@login_required()
def home (request):
    try:
        student = Student.objects.get(user=request.user)
        return render(request, "skoolos/home.html",  {'classes': student.confirmed.all()})
    except Student.DoesNotExist:
        pass

    try:
        teacher = Teacher.objects.get(user=request.user)
        return render(request, "skoolos/home.html",  {'classes': teacher.classes})
    except Teacher.DoesNotExist:
        pass

    return render(request, "skoolos/home.html")

@login_required()
def profile (request):
    pass

def classDetail (request, id):
    classObj = Class.objects.get(id=id)
    return redirect('/')
