from django.urls import path

from . import views

# Essa variável diz a qual app pertence a url dinâmica nos templates
# https://docs.djangoproject.com/en/5.1/intro/tutorial03/#namespacing-url-names
app_name = "projects"
# Essa lista deve conter as rotas para as funcoes definidas em projects/views.py
urlpatterns = [
    path("", views.ProjectListView.as_view(), name="index"),
    path("project/<int:pk>", views.ProjectDetailView.as_view(), name="project"),
    path("project/add", views.ProjectCreateView.as_view(), name="add_project"),
    path(
        "project/<int:pk>/edit", views.ProjectUpdateView.as_view(), name="edit_project"
    ),
    path(
        "project/<int:pk>/delete",
        views.ProjectDeleteView.as_view(),
        name="delete_project",
    ),
    path(
        "project/<int:project_id>/task/<int:task_id>",
        views.TaskDetailView.as_view(),
        name="task",
    ),
    path(
        "project/<int:project_id>/task/add",
        views.TaskCreateView.as_view(),
        name="add_task",
    ),
    path("task/add", views.TaskCreateView.as_view(), name="add_task_global"),
    path(
        "project/<int:project_id>/task/<int:task_id>/edit",
        views.TaskUpdateView.as_view(),
        name="edit_task",
    ),
    path(
        "project/<int:project_id>/task/<int:task_id>/update-status/",
        views.TaskStatusUpdateView.as_view(),
        name="update_task_status",
    ),
    path(
        "project/<int:project_id>/task/<int:task_id>/delete",
        views.TaskDeleteView.as_view(),
        name="delete_task",
    ),
    path("my-tasks", views.UserTasksListView.as_view(), name="user_tasks"),
]
