from django.contrib import admin
from kurama.models import TaskList, Task, Project

class TaskListAdmin(admin.ModelAdmin):
    """
    Changes admin options and functionality for given model
    """
    fields = ('title', 'updated', 'taskListId', 'selfLink')
    list_display = ('title', 'updated')

admin.site.register(TaskList, TaskListAdmin)

class TaskAdmin(admin.ModelAdmin):
    """
    Changes admin options and functionality for given model
    """
    fields = ('title', 'tag', 'completed', 'notes')
    list_display = ('title', 'tag', 'completed')

admin.site.register(Task, TaskAdmin)

class ProjectAdmin(admin.ModelAdmin):
    """
    Changes admin options and functionality for given model
    """
    fields = ('name', 'tag', 'description', 'status', 'due', 'completed')
    list_display = ('name', 'tag', 'completed')

admin.site.register(Project, ProjectAdmin)
