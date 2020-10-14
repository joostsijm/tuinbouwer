"""general methods"""

from tuinbouwer_sensor import LOGGER, api


def send_log_information():
    """update resource market"""
    LOGGER.info("start gathering sensor data")
    LOGGER.info('get temperature')
    sensor_log = {}
    sensor_log['temperature'] = 21.9
    sensor_log['humidity'] = 60.2
    sensor_log['watt'] = 92.2
    LOGGER.info('finishd gathering sensor data %s', sensor_log)

    LOGGER.info('start sending sensor data')
    api.post_sensor_log(sensor_log)
    LOGGER.info('finished sending sensor data')
