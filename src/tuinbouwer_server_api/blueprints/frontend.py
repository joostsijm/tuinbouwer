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
def spaces_log_day(space_id):
    """Get log of last day from space"""
    space = models.Space.query.get(space_id)
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
        })
    return {
        'id': space.id,
        'logs': logs,
    }

@frontend.route('/spaces/<int:space_id>/log/hour')
def spaces_log_hour(space_id):
    """Get log of last hour from space"""
    space = models.Space.query.get(space_id)
    date_time = datetime.now() - timedelta(hours=1)
    minute_logs = models.MinuteLog.query.order_by(models.MinuteLog.date_time.desc()).filter( \
        models.MinuteLog.space_id == space.id,
        models.MinuteLog.date_time > date_time,
    ).all()
    logs = []
    for log in minute_logs:
        logs.append({
            'id': log.id,
            'date_time': log.date_time,
            'min_temperature': log.min_temperature,
            'max_temperature': log.max_temperature,
            'avg_temperature': log.temperature,
        })
    return {
        'id': space.id,
        'logs': logs,
    }
