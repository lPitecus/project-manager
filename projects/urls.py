from django.urls import path

from . import views

# Essa lista deve conter as rotas para as funcoes definidas em projects/views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:project_id>', views.project, name='project'),
    path('project/<int:project_id>/task/<int:task_id>', views.task, name='task')
]