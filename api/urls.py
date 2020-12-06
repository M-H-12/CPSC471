from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('person/', views.person),
    path('course/', views.course),
    path('prerequisite/', views.prerequisite),
    path('admin/', views.admin),
    path('assignment/', views.assignment)
]