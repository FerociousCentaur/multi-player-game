
from django.contrib import admin
from django.urls import path
from .views import *
from django.shortcuts import HttpResponse

urlpatterns = [
    path('' , home , name="home"),
    path('play/<room_code>' , play , name="play"),
    path('close/' , close_room , name="close_room"),
    path('get_players' , get_players , name="get_players"),
]
