from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Project, Task

class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "related_project", "created_at"]


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
