from django.contrib import admin
from kurama.models import TaskList, Task, Project

admin.site.register(TaskList)

class TaskAdmin(admin.ModelAdmin):
    fields = ('title', 'tag', 'completed')

admin.site.register(Task, TaskAdmin)

admin.site.register(Project)
# Register your models here.
