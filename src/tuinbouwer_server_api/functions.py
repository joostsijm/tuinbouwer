"""Multi purpose functions"""

from datetime import datetime, timedelta

from tuinbouwer_server_api import models


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

def summarize_log(summary_log, start_time, time_delta):
    """Calculate something average"""
    minute_logs = models.MinuteLog.query \
        .filter(models.MinuteLog.date_time <= start_time) \
        .filter(models.MinuteLog.date_time >= start_time - time_delta) \
        .all()

    calculate_min_max_average(summary_log, minute_logs, 'temperature')
    calculate_min_max_average(summary_log, minute_logs, 'humidity')
    calculate_min_max_average(summary_log, minute_logs, 'power')

def calculate_min_max_average(summary_log, logs, attribute):
    """Calculate the min, max, and average of a set"""
    min_value = 1e9
    max_value = -1e9
    total_value = 0
    for log in logs:
        value = getattr(log, attribute)
        total_value += value
        if value <= min_value:
            min_value = value
        if value >= max_value:
            max_value = value

    setattr(summary_log, "min_{}".format(attribute), min_value)
    setattr(summary_log, "max_{}".format(attribute), max_value)
    setattr(summary_log, attribute, round(total_value / len(logs), 2))
