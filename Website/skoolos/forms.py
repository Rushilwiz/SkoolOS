from django import forms
from django.contrib.auth.models import User
from api.models import Student, Teacher
import re

class UserUpdateForm(forms.ModelForm):

    username = forms.CharField(max_length=50, disabled=True)
    first_name = forms.CharField(max_length=50, disabled=True)
    last_name = forms.CharField(max_length=50, disabled=True)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['git']

class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['git']
