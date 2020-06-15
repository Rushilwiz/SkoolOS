from .models import Student, Teacher, Class, Assignment, DefFiles
from .serializers import StudentSerializer, TeacherSerializer, ClassSerializer, AssignmentSerializer, UserSerializer
from rest_framework import generics, viewsets, permissions, response, status
from django.http import Http404
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .permissions import isTeacher, IsOwnerOrReadOnly
from django.shortcuts import render, redirect
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_Class = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_Class = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_Class = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_Class = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # def perform_create(self, serializer):
    #     if(self.request.user.groups.filter(name__in=['teachers']).exists() or self.request.user.is_superuser):
    #         serializer.save(owner=self.request.user)
    #     else:
    #         print("UNAUTHORIZED POST")
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_Class = [permissions.IsAuthenticated, isTeacher, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        if(self.request.user.groups.filter(name__in=['teachers']).exists() or self.request.user.is_superuser):
            serializer.save(owner=self.request.user)
        else:
            print("UNAUTHORIZED POST")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DefFilesViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = DefFiles.objects.all()
#     serializer_class = DefFilesSerializer
#     permissions_Class = [permissions.IsAuthenticatedOrReadOnly]
