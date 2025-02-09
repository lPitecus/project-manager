from django.db import models
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


    def get_absolute_url(self):
        # Quando um formulário for preenchido para criar um objeto desse modelo, retorna a página
        # de detalhes desse projeto
        return reverse('projects:project', kwargs={'pk': self.pk})

class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    related_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Quando um formulário for preenchido para criar um objeto desse modelo, retorna a página
        # de detalhes desse projeto
        return reverse('projects:task', kwargs={'project_id': self.related_project_id, 'task_id': self.id})
