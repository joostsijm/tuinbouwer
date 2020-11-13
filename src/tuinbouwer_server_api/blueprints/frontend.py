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
        log = models.HourLog()
        log.space_id = space.id
        now = functions.round_time(datetime.now(), 60)
        functions.summarize_log(log, now, timedelta(hours=1))
        spaces_dict[space.id] = {
            'name': space.name,
            'min_temp': log.min_temperature,
            'max_temp': log.max_temperature,
            'avg_temp': log.temperature,
        }
    return spaces_dict
