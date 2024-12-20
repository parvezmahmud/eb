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
    path('exam/<str:id>/result', views.result, name='exam-result'),
    path('exam/<str:id>/edit', views.edit_test_and_questions, name="edit-test"),
    path('exam/<str:id>/delete', views.delete_question, name='delete-test'),
    # path('exam/<str:id>/leader-board', views.bunit_per_exam_leaderboard, name='bunit-per-exam-leaderboard'),
    path('dashboard/students', views.students_home, name='dashboard-students-home'),
    path('dashboard/students/pending', views.students_unapproved, name='students-pending'),
    path('dashboard/students/approved', views.students_approved, name='students-approved'),
    path('dashboard/students/archive', views.students_cancelled, name='students-archive'),
    path('dashboard/students/pending/<str:id>/', views.exam_batch_approve, name='exam-batch-students-allow'),
    path('dashboard/students/delete/<str:id>/', views.exam_batch_delete, name='exam-batch-students-delete'),
    path('dashboard/b-unit/create-card', views.create_card_bunit, name='create-card-bunit'),
    path('dashboard/b-unit/<str:id>/edit-card', views.edit_card_bunit, name='edit-card-bunit'),
    path('dashboard/b-unit/<str:id>/delete-card', views.delete_card_bunit, name='delete-card-bunit'),
    path('dashboard/c-unit/create-card', views.create_card_cunit, name='create-card-cunit'),
    path('dashboard/c-unit/<str:id>/edit-card', views.edit_card_cunit, name='edit-card-cunit'),
    path('dashboard/c-unit/<str:id>/delete-card', views.delete_card_cunit, name='delete-card-cunit'),
]
