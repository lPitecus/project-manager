from django.urls import path

from . import views

# Essa lista deve conter as rotas para as funcoes definidas em projects/views.py
urlpatterns = [
    path('', views.index, name='index'),
]