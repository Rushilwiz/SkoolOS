from django.urls import path

from . import views

# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path("class/<int:id>", views.classDetail, name="class"),
]
