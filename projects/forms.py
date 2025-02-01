from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput

from projects.models import Project


# https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/#overriding-the-default-fields
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        labels = {
            'name': 'Nome do projeto',
            'description': 'Descrição do projeto',
        }
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o nome do projeto',
                }
            ),
            'description': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Insira a descrição do projeto',
                }
            )
        }