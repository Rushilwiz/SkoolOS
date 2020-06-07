from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Classes, Assignment, DefFiles
from rest_framework import serializers, permissions

class DefFilesSerializer(serializers.HyperlinkedModelSerializer):
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    class Meta:
        model = DefFiles
        fields = ['name']

class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    files = DefFilesSerializer(many=True, read_only=True,allow_null=True)
    class Meta:
        model = Assignment
        fields = ['name', 'due_date', 'url', 'files']

class ClassesSerializer(serializers.HyperlinkedModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True,allow_null=True)
    class Meta:
        model = Classes
        fields = ['url', 'name','assignments']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    classes = ClassesSerializer(many=True, read_only=True,allow_null=True)
    class Meta:
        model = Student
        fields = ['url', 'first_name', 'last_name', 'grade','webmail','student_id','classes', 'git','repo','ion_user']

class TeacherSerializer(serializers.ModelSerializer):
    classes = ClassesSerializer(many=True, read_only=True,allow_null=True)
    class Meta:
        model = Teacher
        fields = ['url', 'first_name', 'last_name', 'classes','git','ion_user']


