from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('person/', views.person),
    path('course/', views.course),
    path('prerequisite/', views.prerequisite),
    path('admin/', views.admin),
    path('counselor/', views.counselor),
    path('room/', views.room),
    path('textbook/', views.textbook),
    path('teacher/', views.teacher),
    path('offering/', views.offering),
    path('student/', views.student),
    path('assignment/', views.assignment),
    path('counselor_office_hours/', views.counselor_office_hours),
    path('material/', views.material),
    path('schedule/', views.schedule)
]