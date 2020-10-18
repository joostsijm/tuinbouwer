"""general methods"""

from tuinbouwer_sensor import LOGGER, SPACE_ID, api, sensor


def send_log_information():
    """update resource market"""
    LOGGER.info("start gathering humidity and temperature")
    humidity, temperature = sensor.read_sensor()
    LOGGER.info('finished gathering humidity %s and temperature %s', humidity, temperature)
    sensor_log = {}
    sensor_log['space_id'] = SPACE_ID
    sensor_log['temperature'] = temperature
    sensor_log['humidity'] = humidity
    sensor_log['watt'] = 0
    LOGGER.info('finished gathering sensor data %s', sensor_log)

    LOGGER.info('start sending sensor data')
    api.post_sensor_log(sensor_log)
    LOGGER.info('finished sending sensor data')
