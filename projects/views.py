from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from .models import Project, Task
from projects.forms import ProjectForm, TaskForm
from django.contrib import messages


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


def add_project(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data['name']
            project_description = form.cleaned_data['description']

            new_project = Project.objects.create(
                name=project_name,
                description=project_description
            )
            new_project.save()
            messages.success(request, "Projeto criado com sucesso!")
            return HttpResponseRedirect(reverse('projects:project', args=(new_project.pk,)))
    context = {"form": form}
    return render(request, 'projects/add_project.html', context)


def task(request, project_id, task_id):
    current_task = get_object_or_404(Task, pk=task_id)
    current_project = get_object_or_404(Project, pk=project_id)
    context = {
        "current_task": current_task,
        "current_project": current_project,
    }
    return render(request, "projects/task.html", context)


def add_task(request, project_id=None):
    """
    - Se um `project_id` for passado, a task será adicionada diretamente ao projeto correspondente.
    - Se não houver `project_id`, o usuário precisará escolher um projeto antes de criar a task.
    """
    current_project = get_object_or_404(Project, pk=project_id) if project_id else None
    form = TaskForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # Pegando os dados do formulário corretamente usando cleaned_data
            task_name = form.cleaned_data["name"]
            task_description = form.cleaned_data["description"]
            related_project = current_project or form.cleaned_data["related_project"]

            # Criando e salvando a nova task
            new_task = Task.objects.create(
                name=task_name,
                description=task_description,
                related_project=related_project
            )
            new_task.save()
            messages.success(request, "Task criada com sucesso!")

            # Redirecionando para a página do projeto ao qual a task pertence
            return HttpResponseRedirect(reverse('projects:project', args=(related_project.id,)))
        else:
            messages.error(request, "Erro ao criar a task. Verifique os campos preenchidos.")

    context = {
        "form": form,
        "current_project": current_project,
    }
    return render(request, "projects/add_task.html", context)
