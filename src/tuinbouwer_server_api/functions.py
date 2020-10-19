"""Multi purpose functions"""

from datetime import datetime, timedelta


def round_time(date_time=None, round_to=60):
    """Round a datetime object to any time lapse in seconds
    date_time : datetime.datetime object, default now.
    round_to : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if date_time is None:
        date_time = datetime.now()
    seconds = (date_time.replace(tzinfo=None) - date_time.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return date_time + timedelta(0, rounding - seconds, - date_time.microsecond)
