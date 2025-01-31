from django.urls import path

from . import views

# Essa variável diz a qual app pertence a url dinâmica nos templates
# https://docs.djangoproject.com/en/5.1/intro/tutorial03/#namespacing-url-names
app_name = "projects"
# Essa lista deve conter as rotas para as funcoes definidas em projects/views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:project_id>', views.project, name='project'),
    path('project/<int:project_id>/task/<int:task_id>', views.task, name='task')
]