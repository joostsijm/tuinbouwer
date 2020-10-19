"""Module to take start and take care of scheduler jobs"""

from datetime import datetime, timedelta

from flask_apscheduler import APScheduler

from tuinbouwer_server_api import models, functions


scheduler = APScheduler()

def start_jobs():
    """Start jobs"""
    scheduler.add_job(
        id="run_hour_log",
        func=hour_job,
        trigger="interval",
        hours=1,
    )
    scheduler.add_job(
        id="run_day_log",
        func=day_job,
        trigger="interval",
        hours=1,
    )


def hour_job():
    """Hour job method"""
    hour_log = models.HourLog()
    now = functions.round_time(datetime.now(), 60)
    functions.summarize_log(hour_log, now, timedelta(hours=1))
    models.db.session.add(hour_log)
    models.db.session.commit()

def day_job():
    """Day job method"""
    day_log = models.DayLog()
    now = functions.round_time(datetime.now(), 60)
    functions.summarize_log(day_log, now, timedelta(days=1))
    models.db.session.add(day_log)
    models.db.session.commit()

if __name__ == "__main__":
    hour_job.__module__ = "scheduler"
