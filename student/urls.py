from django.urls import path
from . import views
urlpatterns = [
    path('students', views.students_home, name='students-home'),
]