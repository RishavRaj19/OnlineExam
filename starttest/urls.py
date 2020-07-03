from django.urls import path
from . import views

urlpatterns = [
    path('student_test_page', views.student_test_page, name='student_test_page'),
    path('result_page_student', views.result_page_student, name='result_page_student'),
    path('result_page', views.result_page, name='result_page'),
]
