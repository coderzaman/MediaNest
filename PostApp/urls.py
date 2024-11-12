from django.contrib import admin
from django.urls import path,include
from PostApp import views

app_name = 'PostApp'

urlpatterns = [
   path('', views.home, name="home"),
]
