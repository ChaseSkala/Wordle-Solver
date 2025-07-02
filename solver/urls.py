from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "solver"
urlpatterns = [
    path('', views.wordle_solver, name='wordle_solver'),
]