from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('students/', views.StudentList.as_view()),
    path('students/<str:pk>/', views.StudentDetail.as_view()),
    path('teachers/', views.TeacherList.as_view()),
    path('teachers/<str:pk>/', views.TeacherDetail.as_view()),
    path('assignments/', views.AssignmentList.as_view()),
    path('assignments/<str:pk>/', views.AssignmentDetail.as_view()),
    path('classes/', views.ClassList.as_view()),
    path('classes/<str:pk>/', views.ClassDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
