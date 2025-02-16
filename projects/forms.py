from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput, Select, CheckboxSelectMultiple

from projects.models import Project, Task


# https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/#overriding-the-default-fields
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        labels = {
            "name": "Nome do projeto",
            "description": "Descrição do projeto",
        }
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o nome do projeto",
                }
            ),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Insira a descrição do projeto",
                }
            ),
        }


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "related_project",
            "responsible",
            "collaborators",
        ]
        labels = {
            "name": "Nome da Tarefa",
            "description": "Descrição da Tarefa",
            "related_project": "Projeto Relacionado",
            "status": "Status da Tarefa",
            "responsible": "Responsável pela tarefa",
        }
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o nome da tarefa",
                }
            ),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
            "status": Select(attrs={"class": "form-select"}),
            "related_project": Select(attrs={"class": "form-select"}),
            "responsible": Select(attrs={"class": "form-select"}),
            "collaborators": CheckboxSelectMultiple(),
        }
