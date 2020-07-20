import datetime
import time


def get_date():
    return datetime.datetime.today().strftime('%Y-%m-%d')


def get_weekday():
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    return days[datetime.datetime.today().weekday()]
