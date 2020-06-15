from django.urls import path
from rest_framework import routers
from api import views as api_views
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'students', api_views.StudentViewSet)
router.register(r'teachers', api_views.TeacherViewSet)
router.register(r'assignments', api_views.AssignmentViewSet)
router.register(r'classes', api_views.ClassViewSet)
# router.register(r'files', api_views.DefFilesViewSet)
router.register(r'users', api_views.UserViewSet)

from users import views as user_views
from users.forms import LoginForm

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include('skoolos.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', user_views.logout, name='logout'),
    path('register/', user_views.register, name='register'),
    path('create_account/', user_views.create_account, name='create_account'),
    path('callback/', user_views.callback, name='callback'),
]
