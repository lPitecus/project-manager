from django.contrib import admin
from .models import Project, Task

class TaskInline(admin.StackedInline):
    model = Task
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    inlines = [TaskInline]


class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "related_project", "created_at"]
    search_fields = ["name"]
    list_editable = ["related_project"]
    list_filter = ["related_project"]

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
