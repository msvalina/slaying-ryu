from datetime import date, timedelta
from calendar import monthrange

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
    elif time_range == "thisquarter":
        start_date = date(today.year, today.month - 1, 1)
        num_of_days_in_quarter = monthrange(today.year, today.month - 1)[1]
        end_date = start_date + timedelta(days=num_of_days_in_month - 1)

    else:
        # set this week
        offset = (today.weekday() + 1) % 7 + 1
        last_saturday = today - timedelta(days=offset)
        start_date = last_saturday
        end_date = today

    return start_date, end_date
