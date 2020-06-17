from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages

from django.contrib.auth.models import User

from .forms import (
    UserUpdateForm,
    StudentUpdateForm,
    TeacherUpdateForm,
    ClassCreationForm,
)

from api.models import Student, Teacher, Class, Assignment

# Create your views here.

@login_required()
def home (request):
    try:
        student = request.user.student
        return render(request, "skoolos/home.html",  {'classes': student.confirmed.all(), 'isTeacher': False})
    except Student.DoesNotExist:
        pass

    try:
        teacher = request.user.teacher
        return render(request, "skoolos/home.html",  {'classes': teacher.classes.all(), 'isTeacher': True})
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
        student = request.user.student
    except Student.DoesNotExist:
        pass
    else:
        if classObj.confirmed.filter(user=student.user).count() != 1:
            return redirect('/')
        else:
            return render(request, "skoolos/class_detail.html", {'class': classObj,'assignments': classObj.assignments.all(), 'teachers': classObj.classes.all(), 'isTeacher': False})

    try:
        teacher = request.user.teacher
    except Teacher.DoesNotExist:
        pass
    else:
        if teacher.classes.filter(id=classObj.id).count() != 1:
            return redirect('/')
        else:
            return render(request, "skoolos/class_detail.html", {'class': classObj,'assignments': classObj.assignments.all(), 'teachers': classObj.classes.all(), 'isTeacher': True})

    return redirect('/')

@login_required()
def profile (request):
    try:
        student = request.user.student
        return student_profile(request)
    except Student.DoesNotExist:
        pass

    try:
        teacher = request.user.teacher
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
        'classes': request.user.student.confirmed.all(),
        'isTeacher': False,
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
        'classes': request.user.teacher.classes.all(),
        'isTeacher': True,
    }

    return render(request, 'skoolos/profile_teacher.html', context)

@login_required()
def createClass (request):
    try:
        teacher = request.user.teacher
    except Teacher.DoesNotExist:
        pass
    else:
        return createClassHelper(request)

    return redirect('/')

def createClassHelper(request):
    teacher = request.user.teacher

    if request.method == "POST":
        classForm = ClassCreationForm(request.POST)
        if classForm.is_valid():
            cleaned_data = classForm.clean()
            print(cleaned_data)
            newClass = classForm.save(commit=False)
            newClass.owner = request.user
            newClass.teacher = request.user.username
            newClass.name = cleaned_data['subject'].replace(' ', '')[:8].lower() + str(cleaned_data['period']) + "_" + teacher.user.username.lower()
            newClass.save()
            classObj = classForm.save_m2m()
            messages.success(request, cleaned_data['subject'].capitalize() + " has been created!")
            print (newClass)
            teacher.classes.add(newClass)
            for student in newClass.unconfirmed.all():
                if student.added_to == "":
                    student.added_to = newClass.name
                else:
                    student.added_to = student.added_to + "," + newClass.name
                student.save()
            return redirect('home')
    else:
        classForm = ClassCreationForm()

    context = {
        'teacher': teacher,
        'classes': teacher.classes.all(),
        'classForm': classForm

    }

    return render(request, "skoolos/createClass.html", context)
