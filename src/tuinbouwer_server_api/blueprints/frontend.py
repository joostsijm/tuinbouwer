"""Frontend blueprint"""

from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError
from flask import Blueprint, abort, request

from tuinbouwer_server_api import models, functions


frontend = Blueprint('frontend', __name__, url_prefix='/frontend')

@frontend.route('/spaces')
def spaces():
    """Get spaces"""
    spaces = models.Space.query.all()
    spaces_dict = {}
    for space in spaces:
        spaces_dict[space.id] = {
            'name': space.name,
        }
    return spaces_dict

@frontend.route('/spaces/overview')
def spaces_overview():
    """Get spaces overview"""
    spaces = models.Space.query.all()
    spaces_dict = {}
    for space in spaces:
        log = models.HourLog.query.order_by(models.HourLog.date_time.desc()).first()
        spaces_dict[space.id] = {
            'id': space.id,
            'name': space.name,
            'min_temperature': log.min_temperature,
            'max_temperature': log.max_temperature,
            'avg_temperature': log.temperature,
            'date_time': log.date_time,
        }
    return spaces_dict

@frontend.route('/spaces/<int:space_id>/log/day')
@frontend.route('/spaces/<int:space_id>/log/day/<int:timestamp>')
def spaces_log_day(space_id, timestamp=None):
    """Get day logs from space"""
    space = models.Space.query.get(space_id)
    if timestamp:
        date_time = datetime.fromtimestamp(timestamp)
    else:
        date_time = datetime.now() - timedelta(days=31)
    day_logs = models.DayLog.query.order_by(models.MinuteLog.date_time.desc()).filter( \
        models.DayLog.space_id == space.id,
        models.DayLog.date_time > date_time,
    ).all()
    logs = []
    for log in day_logs:
        logs.append({
            'id': log.id,
            'date_time': log.date_time,
            'min_temperature': log.min_temperature,
            'max_temperature': log.max_temperature,
            'avg_temperature': log.temperature,
            'min_humidity': log.min_humidity,
            'max_humidity': log.max_humidity,
            'avg_humidity': log.humidity,
        })
    return {
        'id': space.id,
        'logs': logs,
    }

@frontend.route('/spaces/<int:space_id>/log/hour')
@frontend.route('/spaces/<int:space_id>/log/hour/<int:timestamp>')
def spaces_log_hour(space_id, timestamp=None):
    """Get hour logs from space"""
    space = models.Space.query.get(space_id)
    if timestamp:
        date_time = datetime.fromtimestamp(timestamp)
    else:
        date_time = datetime.now() - timedelta(days=1)
    hour_logs = models.HourLog.query.order_by(models.MinuteLog.date_time.desc()).filter( \
        models.HourLog.space_id == space.id,
        models.HourLog.date_time > date_time,
    ).all()
    logs = []
    for log in hour_logs:
        logs.append({
            'id': log.id,
            'date_time': log.date_time,
            'min_temperature': log.min_temperature,
            'max_temperature': log.max_temperature,
            'avg_temperature': log.temperature,
            'min_humidity': log.min_humidity,
            'max_humidity': log.max_humidity,
            'avg_humidity': log.humidity,
        })
    return {
        'id': space.id,
        'logs': logs,
    }

@frontend.route('/spaces/<int:space_id>/log/minute')
@frontend.route('/spaces/<int:space_id>/log/minute/<int:start_timestamp>')
@frontend.route('/spaces/<int:space_id>/log/minute/<int:start_timestamp>/<int:end_timestamp>')
def spaces_log_minute(space_id, start_timestamp=None, end_timestamp=None):
    """Get log of last hour from space"""
    space = models.Space.query.get(space_id)
    if start_timestamp:
        start_date_time = datetime.fromtimestamp(start_timestamp)
    else:
        start_date_time = datetime.now() - timedelta(hours=1)
    if end_timestamp:
        end_date_time = datetime.fromtimestamp(start_timestamp)
    else:
        end_date_time = datetime.now()
    minute_logs = models.MinuteLog.query.order_by(models.MinuteLog.date_time.desc()).filter( \
        models.MinuteLog.space_id == space.id,
        models.MinuteLog.date_time > start_date_time,
        models.MinuteLog.date_time < end_date_time,
    ).all()
    logs = []
    for log in minute_logs:
        logs.append({
            'id': log.id,
            'date_time': log.date_time,
            'avg_temperature': log.temperature,
            'avg_humidity': log.humidity,
        })
    return {
        'id': space.id,
        'logs': logs,
    }
