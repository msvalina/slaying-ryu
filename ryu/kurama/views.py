from datetime import date, timedelta
from calendar import monthrange
from itertools import chain
from operator import attrgetter, itemgetter
from utils import get_date_range
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

def stats(request, time_range=None):

    if time_range is not None:
        time_range = time_range
    elif request.GET.get('time_range'):
        time_range = request.GET.get('time_range', 'thisweek')

    tl_title = request.GET.get('tl', 'all') 
    tag = request.GET.get('tag', 'all')

    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
    else:
        start_date, end_date = get_date_range(time_range)

    if tl_title == "all" and tag == "all":
        tasks = Task.objects.filter(completed__range=[start_date, end_date])
    elif tl_title == "all":
        tasks = Task.objects.filter(completed__range=[start_date, end_date],
                                    tag__icontains=tag)
    elif tag == "all":
        tasks = Task.objects.filter(completed__range=[start_date, end_date],
                                    task_list__title__icontains=tl_title)
    else:
        tasks = Task.objects.filter(completed__range=[start_date, end_date],
                                    task_list__title__icontains=tl_title,
                                    tag__icontains=tag)

    query_info = {'time_range': time_range,
                  'start_date': start_date,
                  'end_date': end_date,
                  'task_lists': tl_title,
                  'tag': tag}

    context = {'query_info': query_info, 'tasks': tasks }

    return render(request, 'kurama/stats.html', context)

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
    # get tasks from current week, week starts from saturday
    today = date.today()
    # offset/delta from current week day till saturday,
    # "last saturday" can't be same as "today"
    offset = (today.weekday() + 1) % 7 + 1
    last_saturday = today - timedelta(days=offset)
    current_week = Task.objects.filter(completed__range=[last_saturday, today])
    date_range = {'start_date': last_saturday, 'end_date': today}
    return render(request, 'kurama/current_week.html', {'tasks': current_week,
                                                 'date_range': date_range})

def populate(request):
    # TODO write date range logic
    call_command('populate_db', 'kurama', interactive=False)
    return render(request, 'kurama/populate.html')

