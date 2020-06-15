from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from api.models import Student, Teacher

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
