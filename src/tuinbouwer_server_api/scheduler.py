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
        trigger="cron",
        minute=0,
    )
    scheduler.add_job(
        id="run_day_log",
        func=day_job,
        trigger="cron",
        hour=0,
    )
    scheduler.add_job(
        id="run_week_log",
        func=week_job,
        trigger="cron",
        day_of_week=0,
    )
    scheduler.add_job(
        id="run_month_log",
        func=month_job,
        trigger="cron",
        day=1,
    )

def hour_job():
    """Hour job method"""
    with scheduler.app.app_context():
        spaces = models.Space.query.all()
        for space in spaces:
            hour_log = models.HourLog()
            hour_log.space_id = space.id
            now = functions.round_time(datetime.now(), 60)
            functions.summarize_log(hour_log, now, timedelta(hours=1))
            models.db.session.add(hour_log)
        models.db.session.commit()

def day_job():
    """Day job method"""
    with scheduler.app.app_context():
        spaces = models.Space.query.all()
        for space in spaces:
            day_log = models.DayLog()
            day_log.space_id = space.id
            now = functions.round_time(datetime.now(), 60)
            functions.summarize_log(day_log, now, timedelta(days=1))
            models.db.session.add(day_log)
        models.db.session.commit()

def week_job():
    """Week job method"""
    with scheduler.app.app_context():
        spaces = models.Space.query.all()
        for space in spaces:
            week_log = models.WeekLog()
            week_log.space_id = space.id
            now = functions.round_time(datetime.now(), 60)
            functions.summarize_log(week_log, now, timedelta(weeks=1))
            models.db.session.add(week_log)
        models.db.session.commit()

def month_job():
    """Month job method"""
    with scheduler.app.app_context():
        spaces = models.Space.query.all()
        for space in spaces:
            month_log = models.MonthLog()
            month_log.space_id = space.id
            now = functions.round_time(datetime.now(), 60)
            functions.summarize_log(month_log, now, timedelta(months=1))
            models.db.session.add(month_log)
        models.db.session.commit()

if __name__ == "__main__":
    hour_job.__module__ = "scheduler"
    day_job.__module__ = "scheduler"
    week_job.__module__ = "scheduler"
    month_job.__module__ = "scheduler"
