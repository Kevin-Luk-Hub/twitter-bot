from datetime import date, datetime, timedelta
import time


def get_date():
    return datetime.today().strftime('%m-%d-%Y')


def get_weekday():
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    return days[datetime.today().weekday()]


def get_previous_dates(days_back):
    start_date = date.today() - timedelta(days=1)
    end_date = start_date - timedelta(days=days_back)
    delta = start_date - end_date
    dates = []

    for i in range(delta.days + 1):
        day = start_date - timedelta(days=i)
        dates.append(day.strftime('%m-%d-%Y'))

    return dates
