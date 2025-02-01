from django import forms


class ProjectForm(forms.Form):
    project_name = forms.CharField(
        label='Nome do Projeto',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do projeto',
            }
        )
    )
    project_description = forms.CharField(
        label='Descrição do projeto',
        required=False,
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do projeto',
            }
        )
    )
