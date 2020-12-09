from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
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
    path('material/', views.material),
    path('schedule/', views.schedule),
    path('teacher_office_hours/', views.teacher_office_hours),
    path('teacher_can_teach/', views.teacher_can_teach),
    path('course_textbook/', views.course_textbook),
    path('offering_room/', views.offering_room),
    path('offering_time/', views.offering_time),
    path('student_textbook/', views.student_textbook),
    path('textbook_author/', views.textbook_author),
    path('counselor_office_hours/', views.counselor_office_hours),
    path('counsels/', views.counsels),
  
    path('', views.StudentListView.as_view()),
    path('<pk>', views.StudentDetailView.as_view())
]