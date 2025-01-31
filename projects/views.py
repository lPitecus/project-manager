from django.shortcuts import render, get_object_or_404
from .models import Project, Task

# Create your views here.
def index(request):
    lista_projetos = Project.objects.order_by("-created_at")
    context = {"lista_projetos": lista_projetos}
    return render(request, "projects/index.html", context)


def project(request, project_id):
    current_project = get_object_or_404(Project, pk=project_id)
    project_tasks = Task.objects.filter(related_project=current_project)
    context = {
        "current_project": current_project,
        "project_tasks": project_tasks
    }
    return render(request, "projects/project.html", context)


def task(request, project_id, task_id):
    current_task = get_object_or_404(Task, pk=task_id)
    current_project = get_object_or_404(Project, pk=project_id)
    context = {
        "current_task": current_task,
        "current_project": current_project,
    }
    return render(request, "projects/task.html", context)