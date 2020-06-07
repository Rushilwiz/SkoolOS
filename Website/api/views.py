from .models import Student, Teacher, Classes, Assignment
from .serializers import StudentSerializer, TeacherSerializer, ClassesSerializer, AssignmentSerializer
from rest_framework import generics, viewsets, permissions

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

class ClassesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer