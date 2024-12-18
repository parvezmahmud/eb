from django.urls import path
from . import views
urlpatterns = [
    path('students', views.students_home, name='students-home'),
    path('students/sign-up', views.signup_user, name='signup'),
    path('students/sign-up/student-info', views.student_info, name='user-info'),
    path('students/profile', views.student_profile, name='profile'),
    path('login', views.user_login, name='login'),
    path('students/logout', views.logout_user, name='logout'),
    path('not-authorized/', views.unauthorized, name='not-authorized'),
    path('students/b-unit', views.student_bunit, name='student-bunit'),
    path('students/c-unit', views.student_cunit, name='student-cunit'),
    path('students/b-unit/leader-board', views.leaderboard_bunit, name='bunit-leaderboard'),
    path('students/c-unit/leader-board', views.leaderboard_cunit, name='cunit-leaderboard')
]