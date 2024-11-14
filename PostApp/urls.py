from django.contrib import admin
from django.urls import path,include
from PostApp import views

app_name = 'PostApp'

urlpatterns = [
   path('', views.home, name="home"),
   path('liked/<pk>/', views.liked, name='liked'),
   path('un-liked/<pk>/', views.un_liked, name='un_liked')
]

