from django.urls import path

from . import views

# Essa variável diz a qual app pertence a url dinâmica nos templates
# https://docs.djangoproject.com/en/5.1/intro/tutorial03/#namespacing-url-names
app_name = "projects"
# Essa lista deve conter as rotas para as funcoes definidas em projects/views.py
urlpatterns = [
    path('', views.ProjectListView.as_view(), name='index'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project'),
    path('project/add', views.ProjectCreateView.as_view(), name='add_project'),
    path('project/<int:project_id>/task/<int:task_id>', views.task, name='task'),
    path('project/<int:project_id>/task/add', views.add_task, name='add_task'),
    path('task/add', views.add_task, name='add_task_global'),

]

