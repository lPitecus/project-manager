from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput, Select, SelectMultiple

from projects.models import Project, Task


# https://docs.djangoproject.com/en/5.1/ref/forms/fields/#iterating-relationship-choices
class UserSelectMultiple(SelectMultiple):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        # Verifica se o valor não é None e obtém o ID correto
        if value is not None and hasattr(value, "value"):
            user_id = value.value  # Captura o ID corretamente
        else:
            user_id = value  # Caso seja um número normal
        user = User.objects.get(pk=user_id)  # Obtém o usuário
        option["attrs"][
            "data-avatar"
        ] = user.profile.avatar.url  # Sempre terá um avatar
        return option


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
            "collaborators": "Colaboradores da tarefa",
        }
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "status": Select(attrs={"class": "form-select"}),
            "related_project": Select(attrs={"class": "form-select"}),
            "responsible": Select(attrs={"class": "form-select"}),
            "collaborators": UserSelectMultiple(
                attrs={
                    "class": "js-example-basic-multiple",
                    "name": "collaborators[]",
                    "multiple": "multiple",
                }
            ),
        }
