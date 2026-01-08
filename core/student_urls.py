from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
