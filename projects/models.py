from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Quando duas ou mais propriedades de um modelo se referem a um mesmo outro modelo, o kwarg
    # related_name deve ser passado.
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='projects_created')
    last_edited_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='last_edited_projects')
    def __str__(self):
        return self.name


    def get_absolute_url(self):
        # Quando um formulário for preenchido para criar um objeto desse modelo, retorna a página
        # de detalhes desse projeto
        return reverse('projects:project', kwargs={'pk': self.pk})

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'A Fazer'),
        ('IN PROGRESS', 'Fazendo'),
        ('PAUSED', 'Pausado'),
        ('DONE', 'Concluído'),
        ('CANCELED', 'Cancelado')
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='TODO'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    related_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tasks_created')
    last_edited_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='last_edited_tasks')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Quando um formulário for preenchido para criar um objeto desse modelo, retorna a página
        # de detalhes desse projeto
        return reverse('projects:task', kwargs={'project_id': self.related_project_id, 'task_id': self.id})
