"""""Frontend blueprint"""

from datetime import date, datetime, timedelta

from flask import Blueprint, json

from tuinbouwer_server_api import models, functions, openai


blueprint = Blueprint('api_frontend', __name__, url_prefix='/api/frontend')


@blueprint.route('/spaces')
def spaces_index():
    """Get spaces"""
    spaces = models.Space.query.all()
    spaces_dict = {}
    for space in spaces:
        spaces_dict[space.id] = {
            'name': space.name,
        }
    return spaces_dict


@blueprint.route('/spaces/overview')
def spaces_overview():
    """Get spaces overview"""
    spaces = models.Space.query.all()
    spaces_dict = {}
    for space in spaces:
        spaces_dict[space.id] = {
            'id': space.id,
            'name': space.name
        }
        hour_log = space.hour_logs.order_by(models.HourLog.date_time.desc()).first()
        if hour_log:
            spaces_dict[space.id]['min_temperature'] = hour_log.min_temperature
            spaces_dict[space.id]['max_temperature'] = hour_log.max_temperature
            spaces_dict[space.id]['avg_temperature'] = hour_log.temperature
            spaces_dict[space.id]['min_humidity'] = hour_log.min_humidity
            spaces_dict[space.id]['max_humidity'] = hour_log.max_humidity
            spaces_dict[space.id]['avg_humidity'] = hour_log.humidity
            spaces_dict[space.id]['date_time'] = hour_log.date_time
    return spaces_dict


@blueprint.route('/spaces/<int:space_id>/log/day')
@blueprint.route('/spaces/<int:space_id>/log/day/<int:timestamp>')
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


@blueprint.route('/spaces/<int:space_id>/log/hour')
@blueprint.route('/spaces/<int:space_id>/log/hour/<int:timestamp>')
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


@blueprint.route('/spaces/<int:space_id>/log/minute')
@blueprint.route('/spaces/<int:space_id>/log/minute/<int:start_timestamp>')
@blueprint.route('/spaces/<int:space_id>/log/minute/<int:start_timestamp>/<int:end_timestamp>')
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


@blueprint.route('/spaces/<int:space_id>/advice')
def spaces_advice(space_id):
    """Get log of last hour from space"""
    space = models.Space.query.get(space_id)
    plant = space.plants.first()
    log = models.SensorLog()
    log.space_id = space_id
    functions.summarize_log(log, functions.round_time(datetime.today(), 60), timedelta(weeks=1))

    message_history = [
        {
            'role': 'user',
            'content': 'You play the role of the grow tool of a horticulturalist. '
                       'You advice me on a plant based on the following information: '
                       'The specie is ' + plant.specie + ', '
                       'it is ' + str((date.today() - plant.germination_date).days) + ' days since germination, '
                       'last week temperature was maximum ' + str(log.max_temperature) + ', minimum ' + str(log.min_temperature) + ', and average ' + str(log.temperature) + ' degree Celsius.'
                       'last week humidity was maximum ' + str(log.max_humidity) + ', minimum ' + str(log.min_humidity) + ', and average ' + str(log.humidity) + ' percent relative humidity. '
                       'Only reply a list of advice for short-term environmental adjustments for the plant.'
                       'Format your reply as a JSON array containing strings.'
        },
    ]
    completion = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=message_history)
    return json.loads(completion.choices[0].message.content)
