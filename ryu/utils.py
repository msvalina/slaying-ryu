from datetime import date, timedelta
from calendar import monthrange
from collections import OrderedDict

def get_date_range(time_range):
    start_date = None
    end_date = None
    today = date.today()
    if time_range == "thisweek":
        # offset/delta from current week day till saturday,
        # "last saturday" can't be same as "today"
        offset = (today.weekday() + 1) % 7 + 1
        last_saturday = today - timedelta(days=offset)
        start_date = last_saturday
        end_date = today
    elif time_range == "lastweek":
        offset = (today.weekday() + 2) % 7 + 1
        friday = today - timedelta(days=offset)
        saturday = friday - timedelta(days=6)
        start_date = saturday
        end_date = friday
    elif time_range == "thismonth":
        start_date = date(today.year, today.month, 1)
        num_of_days_in_month = monthrange(today.year, today.month)[1]
        end_date = start_date + timedelta(days=num_of_days_in_month - 1)
    elif time_range == "lastmonth":
        start_date = date(today.year, today.month - 1, 1)
        num_of_days_in_month = monthrange(today.year, today.month - 1)[1]
        end_date = start_date + timedelta(days=num_of_days_in_month - 1)
    # This does not work :D
    elif time_range == "thisquarter":
        start_date = date(today.year, today.month - 1, 1)
        num_of_days_in_quarter = monthrange(today.year, today.month - 1)[1]
        end_date = start_date + timedelta(days=num_of_days_in_quarter - 1)

    else:
        # set this week
        offset = (today.weekday() + 1) % 7 + 1
        last_saturday = today - timedelta(days=offset)
        start_date = last_saturday
        end_date = today

    return start_date, end_date

def calc_pie_chart_data(tasks):
    xdata_unfiltered = []
    ydata = []
    for task in tasks:
        xdata_unfiltered += [task.tag]
    # filter out duplicates
    xdata = list(OrderedDict.fromkeys(xdata_unfiltered))

    # count number of repeated tags and save it to ydata
    counter = 0
    for i in range(0, len(xdata)):
        for j in range(0, len(xdata_unfiltered)):
            if xdata[i] == xdata_unfiltered[j]:
                counter += 1
        ydata.append(counter)
        counter = 0

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
            'tag_script_js': False,
            'jquery_on_ready': False,
        },
    }
    return data
