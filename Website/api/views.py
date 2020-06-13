from .models import Student, Teacher, Classes, Assignment, DefFiles
from .serializers import StudentSerializer, TeacherSerializer, ClassesSerializer, AssignmentSerializer, UserSerializer
from rest_framework import generics, viewsets, permissions, response, status
from django.http import Http404
from rest_framework.views import APIView
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]


class TeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]


class ClassesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

# class DefFilesViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = DefFiles.objects.all()
#     serializer_class = DefFilesSerializer
#     permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
