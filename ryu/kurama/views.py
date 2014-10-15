from datetime import date, timedelta
from itertools import chain
from operator import attrgetter, itemgetter
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.core.management import call_command
from kurama.models import TaskList, Task, Project

def index(request):
    """ Get latest Important and Not important tasks chain and sort querysets
    and return render response """

    latest_imds = get_list_or_404(Task.objects.order_by('-completed'),
                                  task_list="01-Im&Ds")[:5]
    latest_imnds = get_list_or_404(Task.objects.order_by('-completed'),
                                   task_list="02-Im&Nds")[:5]
    latest_im = sorted(chain(latest_imds, latest_imnds),
                       key=attrgetter('completed'),
                       reverse=True)[:5]

    latest_nids = get_list_or_404(Task.objects.order_by('-completed'),
                                  task_list="03-Ni&Ds")[:5]
    latest_ninds = get_list_or_404(Task.objects.order_by('-completed'),
                                   task_list="04-Ni&Nds")[:5]
    latest_ni = sorted(chain(latest_nids, latest_ninds),
                       key=attrgetter('completed'), 
                       reverse=True)[:5]

    tasklists = get_list_or_404(TaskList.objects.all())

    # TODO Implement in models.py Task, function for returning popular projects
    projects = get_list_or_404(Project)
    numb_of_task_per_project = {}
    for proj in projects:
        count = Task.objects.filter(tag_name=proj.name,
                                    task_list__title__contains="Im").count()
        numb_of_task_per_project[proj.name] = count
    # popular projects by number of completed tasks
    popular_projects = []
    popular_projects = sorted(numb_of_task_per_project.items(),
                              key=itemgetter(1),
                              reverse=True)[:10]

    projects = [x[0] for x in popular_projects]

    context = {'latest_im_tasks': latest_im,
               'latest_ni_tasks': latest_ni,
               'tasklists': tasklists,
               'projects': projects}

    return render(request, 'kurama/index.html', context)

def detail(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    return render(request, 'kurama/detail.html', {'task': task})

def task_list(request, task_list):
    tasks = get_list_or_404(Task, task_list=task_list)
    context = {'task_list': task_list,
               'tasks': tasks}
    return render(request, 'kurama/task_list.html', context)

def tag(request, tag):
    tasks = get_list_or_404(Task, tag=tag)
    context = {'tag': tag,
               'tasks': tasks}
    return render(request, 'kurama/tag.html', context)

def tagname(request, tagname):
    tasks = get_list_or_404(Task, tag_name=tagname)
    context = {'tag': tagname,
               'tasks': tasks}
    return render(request, 'kurama/tag.html', context)

def stats(request):
    tasks = get_list_or_404(Task.objects.all())
    return render(request, 'kurama/stats.html', {'tasks': tasks})

def about(request):
    return render(request, 'kurama/about.html')

def graph(request):
    """
    pieChart example
    """
    projects = Project.objects.all()
    numb_of_task_per_project = {}
    for proj in projects:
        count = Task.objects.filter(tag_name=proj.name,
                                    task_list__title__contains="Im").count()
        numb_of_task_per_project[proj.name] = count
    # popular projects by number of completed tasks
    popular_projects = []
    popular_projects = sorted(numb_of_task_per_project.items(),
                              key=itemgetter(1),
                              reverse=True)[:10]

    xdata = [x[0] for x in popular_projects]
    ydata = [x[1] for x in popular_projects]

    color_list = ['#5d8aa8', '#e32636', '#efdecd', '#ffbf00', '#ff033e',
                  '#a4c639', '#b2beb5', '#8db600', '#7fffd4', '#ff007f',
                  '#ff55a3', '#5f9ea0']
    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " tasks"},
        "color_list": color_list
    }
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'  # container name

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }

    return render_to_response('kurama/graph.html', data)

def current_week(request):
    today = date.today()
    # TODO write date range logic
    tasks = get_list_or_404(Task, completed__range=["2014-08-01", "2014-10-31"])
    return render(request, 'kurama/current_week.html', {'tasks': tasks})

def last_week(request):
    today = date.today()
    # TODO write date range logic
    tasks = get_list_or_404(Task, completed__range=["2014-08-01", "2014-10-31"])
    return render(request, 'kurama/last_week.html', {'tasks': tasks})

def last_month(request):
    # TODO write date range logic
    tasks = get_list_or_404(Task, completed__range=["2014-08-01", "2014-10-31"])
    return render(request, 'kurama/last_month.html', {'tasks': tasks})

def last_quarter(request):
    today = date.today()
    # TODO write date range logic
    tasks = get_list_or_404(Task, completed__range=["2014-08-01", "2014-10-31"])
    return render(request, 'kurama/last_quarter.html', {'tasks': tasks})

def last_year(request):
    today = date.today()
    # TODO write date range logic
    tasks = get_list_or_404(Task, completed__range=["2014-08-01", "2014-10-31"])
    return render(request, 'kurama/last_year.html', {'tasks': tasks})

def populate(request):
    # TODO write date range logic
    call_command('populate_db', 'kurama', interactive=False)
    return render(request, 'kurama/populate.html')

