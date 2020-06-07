from django.urls import path
from rest_framework import routers
from api import views
from django.contrib import admin
from django.conf.urls import include

router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'classes', views.ClassesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),

]