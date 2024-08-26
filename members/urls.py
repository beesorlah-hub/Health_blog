from django.contrib import admin
from django.urls import path, include
from .views import UserRegisterView
urlpatterns = [
   
    path('Register/', UserRegisterView.as_view(), name='register'),

]
