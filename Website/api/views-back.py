from .models import Student, Teacher, Classes, Assignment, DefFiles
from .serializers import StudentSerializer, TeacherSerializer, ClassesSerializer, AssignmentSerializer, UserSerializer
from rest_framework import generics, viewsets, permissions, response, status
from django.http import Http404
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .permissions import isTeacher, IsOwnerOrReadOnly
from django.shortcuts import render, redirect
from rest_framework.parsers import JSONParser 
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import mixins


class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StudentDetail(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permissions_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    def perform_create(self, serializer):
        if(self.request.user.groups.filter(name__in=['teachers']).exists() or self.request.user.is_superuser):
            serializer.save(owner=self.request.user)
        else:
            print("UNAUTHORIZED POST")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherDetail(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permissions_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    
class ClassesList(generics.ListCreateAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    #permissions_classes = [isTeacher]
    def perform_create(self, serializer):
        if(self.request.user.groups.filter(name__in=['teachers']).exists() or self.request.user.is_superuser):
            serializer.save(owner=self.request.user)
        else:
            print("UNAUTHORIZED POST")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ClassesDetail(generics.RetrieveAPIView):
#     queryset = Classes.objects.all()
#     serializer_class = ClassesSerializer
#     # permissions_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class ClassesDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        print(self.owner)
        if(request.user == self.owner):
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AssignmentList(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    def perform_create(self, serializer):
        if(self.request.user.groups.filter(name__in=['teachers']).exists() or self.request.user.is_superuser):
            serializer.save(owner=self.request.user)
        else:
            print("UNAUTHORIZED POST")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignmentDetail(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permissions_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
