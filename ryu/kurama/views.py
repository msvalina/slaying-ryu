from django.http import Http404
from django.shortcuts import render
from kurama.models import TaskList, Task, Project

def index(request):
    latest_tasks = Task.objects.order_by('-completed')[:15]
    context = {'latest_tasks': latest_tasks}
    return render(request, 'kurama/index.html', context)

def detail(request, taskList_id):
    try:
        taskList_id = Task.objects.filter(taskList_id=taskList_id)
    except taskList_id.DoesNotExist:
        raise Http404
    return render(request, 'kurama/detail.html', {'tlid': taskList_id})
