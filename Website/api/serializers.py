from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Classes, Assignment, DefFiles
from rest_framework import serializers, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly,isTeacher

class UserSerializer(serializers.HyperlinkedModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())
    teachers = serializers.PrimaryKeyRelatedField(many=True, queryset=Teacher.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username']

# class DefFilesSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = DefFiles
#         fields = ['name', 'path','assignment','classes', "teacher",'url', 'id']

class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    #permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    # files = DefFilesSerializer(many=True, read_only=True,allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Assignment
        # fields = ['url','name', 'due_date', 'path' , "classes","teacher",'owner']
        fields = ['name', 'due_date', 'path' , "classes","teacher",'owner']

class ClassesSerializer(serializers.HyperlinkedModelSerializer):
    # assignments = AssignmentSerializer(many=True, read_only=True,allow_null=True)
    # default_file=DefFilesSerializer(many=True, read_only=True,allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Classes
        # fields = ['url','name', 'repo','path', "teacher",'assignments',"default_file", 'confirmed', 'unconfirmed','owner']
        fields = ['name', 'repo','path', "teacher",'assignments',"default_file", 'confirmed', 'unconfirmed','owner']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    # classes = ClassesSerializer(many=True, read_only=True,allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Student
        # fields = ['url','first_name', 'last_name', 'grade','email','student_id', 'git','ion_user','classes','added_to','completed', 'repo','owner']
        fields = ['grade','email','student_id', 'git','ion_user','classes','added_to','completed', 'repo','owner']

class TeacherSerializer(serializers.ModelSerializer):
    # classes = ClassesSerializer(many=True, read_only=True,allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Teacher
        # fields = ['url','first_name', 'last_name','git','ion_user', 'email','classes','owner']
        fields = ['first_name', 'last_name','git','ion_user', 'email','classes','owner']


