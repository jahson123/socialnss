import datetime as dt
from math import floor


def date_cal(date):
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_now = dt.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    date = dt.datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
    new_date = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    result = str(new_now - new_date)
    if 'day' in result:
        result.split(',')
        days = result.split('day')
        if 1 <= int(days[0]) < 31:
            return "{} days ago".format(int(days[0]))
        elif 31 <= int(days[0]) <= 334:
            month = floor(int(days[0]) / 30)
            return "{} months ago".format(month)
        elif days > 334:
            lasted = dt.datetime.now().strftime('%B %d %Y')
            return lasted
    elif 'day' not in result:
        time = result.split(':')
        if 1 <= int(time[0]) <= 23:
            return "{} hours ago".format(int(time[0]))
        elif 1 <= int(time[1]) <= 59:
            return "{} minutes ago".format(int(time[1]))
        else:
            return "just now"
