from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Classes, Assignment, DefFiles
from rest_framework import serializers, permissions
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = User
        fields = ['id', 'username', 'students']

# class DefFilesSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = DefFiles
#         fields = ['name', 'path','assignment','classes', "teacher",'url', 'id']

class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
    #permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    # files = DefFilesSerializer(many=True, read_only=True,allow_null=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    owner = serializers.ReadOnlyField(source='owner.username')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Assignment
        fields = ['url','name', 'due_date', 'path' , "classes","teacher",'owner']

class ClassesSerializer(serializers.HyperlinkedModelSerializer):
    # assignments = AssignmentSerializer(many=True, read_only=True,allow_null=True)
    # default_file=DefFilesSerializer(many=True, read_only=True,allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    class Meta:
        model = Classes
        fields = ['url', 'name', 'repo','path', "teacher",'assignments',"default_file", 'confirmed', 'unconfirmed','owner']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    # classes = ClassesSerializer(many=True, read_only=True,allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    class Meta:
        model = Student
        fields = ['url', 'first_name', 'last_name', 'grade','email','student_id', 'git','ion_user','classes','added_to','completed', 'repo','owner']

class TeacherSerializer(serializers.ModelSerializer):
    # classes = ClassesSerializer(many=True, read_only=True,allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    class Meta:
        model = Teacher
        fields = ['url', 'first_name', 'last_name','git','ion_user', 'email','classes','owner']


