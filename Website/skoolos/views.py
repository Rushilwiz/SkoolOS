from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages

from django.contrib.auth.models import User

from .forms import UserUpdateForm, StudentUpdateForm, TeacherUpdateForm

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
        return render(request, "skoolos/home.html",  {'classes': teacher.classes.all()})
    except Teacher.DoesNotExist:
        pass

    return render(request, "skoolos/home.html")

@login_required()
def profile (request):
    pass

@login_required()
def classDetail (request, id):
    classObj = Class.objects.get(id=id)

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        pass
    else:
        if classObj.confirmed.filter(user=student.user).count() != 1:
            return redirect('/')
        else:
            return render(request, "skoolos/class_detail.html", {'class': classObj,'assignments': classObj.assignments.all(), 'teachers': classObj.classes.all()})

    try:
        teacher = Teacher.objects.get(user=request.user)
        return render(request, "skoolos/home.html",  {'classes': teacher.classes.all()})
    except Teacher.DoesNotExist:
        pass
    else:
        if classObj.confirmed.filter(user=student.user).count() != 1:
            return redirect('/')
        else:
            return render(request, "skoolos/class_detail.html", {'class': classObj,'assignments': classObj.assignments.all(), 'teachers': classObj.classes.all()})

    return redirect('/')

@login_required()
def profile (request):
    try:
        student = Student.objects.get(user=request.user)
        return student_profile(request)
    except Student.DoesNotExist:
        pass

    try:
        teacher = Teacher.objects.get(user=request.user)
        return teacher_profile(request)
    except Teacher.DoesNotExist:
        pass

    return redirect("/")

def student_profile (request):
    if request.method == "POST":
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = StudentUpdateForm(request.POST,
                                        instance=request.user.student)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, "Your account has been updated!")
            return redirect('profile')
    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = StudentUpdateForm(instance=request.user.student)

    context = {
        'userForm': userForm,
        'profileForm': profileForm,
        'classes': request.user.student.confirmed.all()
    }

    return render(request, 'skoolos/profile_student.html', context)

def teacher_profile (request):
    if request.method == "POST":
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = TeacherUpdateForm(request.POST,
                                        instance=request.user.teacher)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, "Your account has been updated!")
            return redirect('profile')
    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = TeacherUpdateForm(instance=request.user.teacher)

    context = {
        'userForm': userForm,
        'profileForm': profileForm,
        'classes': request.user.teacher.classes.all()
    }

    return render(request, 'skoolos/profile_teacher.html', context)
