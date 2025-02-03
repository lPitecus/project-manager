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
    Essa view tem comportamento dinâmico. Se ela for acessada via url task/add, ela não recebe o parametro project_id.
    Isso significa que ela foi acessada fora de um projeto, e o campo de projeto relacionado na criação da task será
    mostrado ao usuário. Caso essa view seja acessada pela url projects/<project_id>/task/add, ela recebe o parametro
    project_id para definir automaticamente o campo related_project sem mostrar ao usuário.
    :param request:
    :param project_id:
    :return:
    """

    project = None
    form = TaskForm()

    if project_id:
        project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Criamos a task sem salvar imediatamente

            # Definir o projeto relacionado com base no que veio no POST
            if project:
                task.related_project = project
            else:
                related_project_id = request.POST.get("related_project")
                if related_project_id:
                    task.related_project = get_object_or_404(Project, id=related_project_id)
                else:
                    messages.error(request, "Selecione um projeto para a tarefa.")
                    return render(request, "projects/add_task.html", {"form": form, "current_project": project})

            task.save()
            messages.success(request, "Task criada com sucesso!")

            return HttpResponseRedirect(reverse('projects:project', args=(task.related_project.id,)))

    context = {
        'form': form,
        'current_project': project
    }
    return render(request, 'projects/add_task.html', context)

