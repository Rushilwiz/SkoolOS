from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Classes, Assignment
from rest_framework import serializers

class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assignment
        fields = ['name', 'due_date', 'url']

class ClassesSerializer(serializers.HyperlinkedModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True,allow_null=True)
    class Meta:
        model = Classes
        fields = ['url', 'name','assignments']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    classes = ClassesSerializer(many=True, read_only=True,allow_null=True)
    class Meta:
        model = Student
        fields = ['url', 'first_name', 'last_name', 'grade','webmail','student_id','classes']

class TeacherSerializer(serializers.ModelSerializer):
    classes = ClassesSerializer(many=True, read_only=True,allow_null=True)
    class Meta:
        model = Teacher
        fields = ['url', 'first_name', 'last_name', 'classes']


