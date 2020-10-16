"""Page blueprint"""

from flask import Blueprint, abort, request

from tuinbouwer_server_api import models


sensor_api = Blueprint('sensor_api', __name__, url_prefix='/sensor_api/v1')

@sensor_api.route('/', methods=(['POST']))
def get_sensor_log():
    """Route to POST sensor data"""
    sensor_log = models.SensorLog()
    sensor_log.temperature = request.form.get('temperature')
    sensor_log.humidity = request.form.get('humidity')
    sensor_log.power = request.form.get('power')
    sensor_log.space_id = request.form.get('space_id')
    models.db.session.add(sensor_log)
    models.db.session.commit()
    return {
        'temperature': str(sensor_log.temperature),
        'humidity': str(sensor_log.humidity),
        'power': str(sensor_log.power),
        'space_id': sensor_log.space_id,
    }

@sensor_api.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return abort(404)
