from datetime import date, timedelta
from itertools import chain
from operator import attrgetter
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from kurama.models import TaskList, Task, Project

def index(request):
    """ Get latest Important and Not important tasks chain and sort querysets
    and return render response """
    latest_imds_tasks = get_list_or_404(Task, task_list="01-Im&Ds")[:5]
    latest_imnds_tasks = get_list_or_404(Task, task_list="02-Im&Nds")[:5]
    latest_im_tasks = sorted(chain(latest_imds_tasks, latest_imnds_tasks),
        key=attrgetter('completed'), reverse=True)[:5]

    latest_nids_tasks = get_list_or_404(Task, task_list="03-Ni&Ds")[:5]
    latest_ninds_tasks = get_list_or_404(Task, task_list="04-Ni&Nds")[:5]
    latest_ni_tasks = sorted(chain(latest_nids_tasks, latest_ninds_tasks),
        key=attrgetter('completed'), reverse=True)[:5]

    tasklists = get_list_or_404(TaskList.objects.all())

    context = {'latest_im_tasks': latest_im_tasks,
               'latest_ni_tasks': latest_ni_tasks,
               'tasklists' : tasklists}

    return render(request, 'kurama/index.html', context)

def detail(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    return render(request, 'kurama/detail.html', {'task': task})

def current_week(request, taskListName):
    today = date.today()
    try:
        taskListName = Task.objects.filter(taskList_id=taskListName,
            completed__range=["2014-08-01", "2014-10-31"])
    except taskListName.DoesNotExist:
        raise Http404
    return render(request, 'kurama/current_week.html',
            {'taskListName': taskListName})

def last_week(request):
    today = date.today()
    try:
        taskList = Task.objects.filter(
            completed__range=["2014-08-01", "2014-10-31"])
    except taskList.DoesNotExist:
        raise Http404
    return render(request, 'kurama/last_week.html',
            {'taskList': taskList})

