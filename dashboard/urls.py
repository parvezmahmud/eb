from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home" ),
    path('dashboard', views.dashboard_home, name="dashboard-home"),
    path('dashboard/b-unit', views.bunit, name='b-unit-home'),
    path('dashboard/c-unit', views.cunit, name='c-unit-home'),
    path('dashboard/b-unit/create-test', views.create_exam_bunit, name="create-exam-bunit"),
    path('dashboard/b-unit/create-test/create-question', views.create_questions_bunit, name="create-question-bunit"),
    path('dashboard/c-unit/create-test', views.create_exam_cunit, name="create-exam-cunit"),
    path('dashboard/c-unit/create-test/create-question', views.create_questions_cunit, name="create-question-cunit"),
    path('exam/<str:id>/', views.ind_exam, name='ind-exam'),
    path('exam/<str:id>/take-exam', views.take_exam, name='take-exam'),
]
