from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('teacher', views.teacher, name='teacher'),
    path('test', views.test, name='test'),
    path('ques_ans', views.ques_ans, name='ques_ans'),
    path('all_tests', views.all_tests, name='all_tests'),
    path('all_tests_student', views.all_tests_student, name='all_tests_student'),

    path('starttest', include('starttest.urls'))
]
