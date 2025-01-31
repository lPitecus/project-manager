from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Task

# Create your views here.
def index(request):
    lista_projetos = Project.objects.order_by("-created_at")
    context = {"lista_projetos": lista_projetos}
    return render(request, "projects/index.html", context)


def project(request, project_id):
    current_project = Project.objects.get(pk=project_id)
    context = {"current_project": current_project}
    return render(request, "projects/project.html", context)