from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import ProjectForm, TaskForm
from .models import Project, Task


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = "/users/login/"
    redirect_field_name = "projects/add_project.html"
    model = Project
    template_name = "projects/add_project.html"
    permission_required = "projects.add_project"
    # O atributo form_class serve apenas para usar as labels e widgets definidos no forms.py.
    # Caso for preferível usar o nome padrão dos campos (definido no models.py), basta comentar a linha abaixo.
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_edited_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Projeto criado com sucesso!")
        return response


class ProjectListView(LoginRequiredMixin, ListView):
    login_url = "/users/login/"
    redirect_field_name = "projects/index.html"
    model = Project
    template_name = "projects/index.html"
    # Numa view genérica, o contexto é criado automaticamente com base no modelo usado e no tipo de genérico usado.
    # Nesse caso, o nome do objeto de contexto é "project_list"
    #                                             ^^^^^^^ ^^^^
    #                                      nome do modelo|nome do tipo de view genérica
    # Caso queira mudar o nome do objeto de contexto, basta mudar o parâmetro context_object_name
    # https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-display/#making-friendly-template-contexts


class ProjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    # A classe genérica DetailView espera que uma chave primária seja passada como um parâmetro
    # na url chamado "pk" por padrão. Isso é usado para determinar qual objeto (nesse caso, um Project) deve
    # ser recuperado do banco de dados.
    login_url = "/users/login/"
    redirect_field_name = "projects/project.html"
    model = Project
    template_name = "projects/project.html"
    context_object_name = "current_project"
    permission_required = "projects.view_project"

    def get_context_data(self, **kwargs):
        # O override do metodo "get_context_data" permite que seja criado um objeto de contexto personalizado, baseado
        # na chave primária passada na url. Isso serve para passar como contexto adicional objetos relacionados ao pk
        # ou algo que não dependa dessa chave primária
        context = super().get_context_data(
            **kwargs
        )  # Linha obrigatória para criar o objeto contexto.
        # Adicionando tarefas relacionadas ao contexto
        context["project_tasks"] = Task.objects.filter(
            related_project=self.object
        ).order_by("-status")
        return context

    # https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-display/#adding-extra-context


class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = "/users/login/"
    redirect_field_name = "projects/edit_project.html"
    model = Project
    template_name = "projects/edit_project.html"
    context_object_name = "current_project"
    permission_required = "projects.change_project"
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.last_edited_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Projeto atualizado com sucesso!")
        return response


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = "/users/login/"
    redirect_field_name = "projects/index.html"
    model = Project
    template_name = "projects/delete_project.html"
    context_object_name = "current_project"
    permission_required = "projects.delete_project"
    success_url = reverse_lazy("projects:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Projeto excluído com sucesso!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_tasks"] = Task.objects.filter(related_project=self.object)
        return context


class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = "/users/login/"
    redirect_field_name = "projects/add_task.html"
    model = Task
    form_class = TaskForm
    template_name = "projects/add_task.html"
    permission_required = "projects.add_task"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if "project_id" in self.kwargs:
            # Remove o campo related_project do formulário quando há project_id na URL
            del form.fields["related_project"]
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("project_id")

        if project_id:
            context["current_project"] = get_object_or_404(Project, id=project_id)

        return context

    def form_valid(self, form):
        project_id = self.kwargs.get("project_id")

        if project_id:
            # Se um project_id foi passado na URL, associa automaticamente a task a esse projeto
            form.instance.related_project = get_object_or_404(Project, id=project_id)
        elif not form.instance.related_project:
            # Se a task for adicionada sem project_id, o usuário deve escolher um projeto manualmente
            messages.error(self.request, "Selecione um projeto para a tarefa.")
            return self.form_invalid(form)

        form.instance.created_by = self.request.user
        form.instance.last_edited_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Task criada com sucesso!")
        return response

    def get_success_url(self):
        return reverse(
            "projects:task", args=[self.object.related_project.id, self.object.id]
        )


class TaskDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = "/users/login/"
    redirect_field_name = "projects/task.html"
    model = Task
    template_name = "projects/task.html"
    context_object_name = "current_task"
    permission_required = "projects.view_task"

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

    def get_success_url(self):
        # Redireciona para a página do projeto relacionado após a criação da tarefa.
        return reverse("projects:project", args=[self.object.related_project.id])


class TaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = "/users/login/"
    redirect_field_name = "projects/edit_task.html"
    model = Task
    template_name = "projects/edit_task.html"
    context_object_name = "current_task"
    permission_required = "projects.change_task"
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.last_edited_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Tarefa atualizada com sucesso!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("project_id")

        # Get the project using the project_id
        context["current_project"] = get_object_or_404(Project, pk=project_id)
        return context

    def get_object(self, queryset=None):
        # Override get_object to retrieve the specific Task object based on task_id and project_id.
        project_id = self.kwargs.get("project_id")
        task_id = self.kwargs.get("task_id")

        # Fetch the specific task that belongs to the given project
        return get_object_or_404(Task, pk=task_id, related_project_id=project_id)


class TaskStatusUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "projects.change_task"

    def post(self, request, project_id, task_id):
        task = get_object_or_404(Task, pk=task_id, related_project_id=project_id)
        new_status = request.POST.get("status")
        valid_statuses = dict(Task.STATUS_CHOICES).keys()

        if new_status in valid_statuses:
            task.status = new_status
            task.last_edited_by = request.user
            task.save()
            messages.success(request, "Status atualizado com sucesso!")
        else:
            messages.error(request, "Status inválido!")

        return redirect("projects:task", project_id=project_id, task_id=task_id)


class TaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = "/users/login/"
    redirect_field_name = "projects/index.html"
    model = Task
    template_name = "projects/delete_task.html"
    context_object_name = "current_task"
    permission_required = "projects.delete_task"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Tarefa excluída com sucesso!")
        return response

    def get_success_url(self):
        return reverse_lazy(
            "projects:project", kwargs={"pk": self.object.related_project_id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("project_id")
        context["current_project"] = get_object_or_404(Project, pk=project_id)
        return context

    def get_object(self, queryset=None):
        # Override get_object to retrieve the specific Task object based on task_id and project_id.
        project_id = self.kwargs.get("project_id")
        task_id = self.kwargs.get("task_id")

        # Fetch the specific task that belongs to the given project
        return get_object_or_404(Task, pk=task_id, related_project_id=project_id)
