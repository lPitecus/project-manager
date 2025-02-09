from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic

from .forms import ProjectForm, TaskForm
from .models import Project, Task


class ProjectListView(generic.ListView):
    model = Project
    template_name = "projects/index.html"
    # Numa view genérica, o contexto é criado automaticamente com base no modelo usado e no tipo de genérico usado.
    # Nesse caso, o nome do objeto de contexto é "project_list"
    #                                             ^^^^^^^ ^^^^
    #                                      nome do modelo|nome do tipo de view genérica
    # Caso queira mudar o nome do objeto de contexto, basta mudar o parâmetro context_object_name
    # https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-display/#making-friendly-template-contexts


class ProjectDetailView(generic.DetailView):
    # A classe genérica DetailView espera que uma chave primária seja passada como um parâmetro
    # na url chamado "pk" por padrão. Isso é usado para determinar qual objeto (nesse caso, um Project) deve
    # ser recuperado do banco de dados.
    model = Project
    template_name = "projects/project.html"
    context_object_name = "current_project"

    def get_context_data(self, **kwargs):
        # O override do metodo "get_context_data" permite que seja criado um objeto de contexto personalizado, baseado
        # na chave primária passada na url. Isso serve para passar como contexto adicional objetos relacionados ao pk
        # ou algo que não dependa dessa chave primária
        context = super().get_context_data(**kwargs)  # Linha obrigatória para criar o objeto contexto.
        # Adicionando tarefas relacionadas ao contexto
        context["project_tasks"] = Task.objects.filter(related_project=self.object)
        return context
    # https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-display/#adding-extra-context


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


class ProjectUpdateView(generic.edit.UpdateView):
    model = Project
    template_name = "projects/edit_project.html"
    context_object_name = "current_project"
    form_class = ProjectForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Projeto atualizado com sucesso!")
        return response


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "projects/task.html"
    context_object_name = "current_task"

    def get_object(self, queryset=None):
        # Override get_object to retrieve the specific Task object based on task_id and project_id.
        project_id = self.kwargs.get("project_id")
        task_id = self.kwargs.get("task_id")

        # Fetch the specific task that belongs to the given project
        return get_object_or_404(Task, pk=task_id, related_project_id=project_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("project_id")

        # Get the project using the project_id
        context["current_project"] = get_object_or_404(Project, pk=project_id)
        return context


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
