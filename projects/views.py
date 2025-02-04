from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy

from .models import Project, Task
from projects.forms import ProjectForm, TaskForm
from django.contrib import messages
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "lista_projetos"


def project(request, project_id):
    current_project = get_object_or_404(Project, pk=project_id)
    project_tasks = Task.objects.filter(related_project=current_project)
    context = {
        "current_project": current_project,
        "project_tasks": project_tasks
    }
    return render(request, "projects/project.html", context)


class ProjectCreateView(generic.edit.CreateView):
    model = Project
    template_name = "projects/add_project.html"
    # O atributo form_class serve apenas para usar as labels e widgets definidos no forms.py.
    # Caso for preferível usar o nome padrão dos campos (definido no models.py), basta comentar a linha abaixo.
    form_class = ProjectForm
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Projeto criado com sucesso!")
        return response


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
