"""Job tests"""

from datetime import datetime, timedelta
import random

from tuinbouwer_server_api import models, functions


def test_average_temperature(flask_client, create_space):
    """Test adding space to database"""
    now = functions.round_time(datetime.now(), 60)
    min_temperature = 1e9
    max_temperature = -1e9
    min_humidity = 1e9
    max_humidity = -1e9
    min_power = 1e9
    max_power = -1e9
    for i in range(1,60):
        sensor_log = models.MinuteLog()
        sensor_log.date_time = now - timedelta(minutes=i)
        sensor_log.temperature = random.randint(10, 40)
        sensor_log.humidity = random.randint(10, 90)
        sensor_log.power = random.randint(100, 1200)
        sensor_log.space_id = 1
        models.db.session.add(sensor_log)
        if sensor_log.temperature <= min_temperature:
            min_temperature = sensor_log.temperature
        if sensor_log.temperature >= max_temperature:
            max_temperature = sensor_log.temperature
        if sensor_log.humidity <= min_humidity:
            min_humidity = sensor_log.humidity
        if sensor_log.humidity >= max_humidity:
            max_humidity = sensor_log.humidity
        if sensor_log.power <= min_power:
            min_power = sensor_log.power
        if sensor_log.power >= max_power:
            max_power = sensor_log.power
    models.db.session.commit()

    hour_log = models.HourLog()
    functions.summarize_log(hour_log, now, timedelta(hours=1))
    assert hour_log.min_temperature == min_temperature, "min temperature is the same"
    assert hour_log.max_temperature == max_temperature, "max temperature is the same"
    assert hour_log.min_humidity == min_humidity, "min humidity is the same"
    assert hour_log.max_humidity == max_humidity, "max humidity is the same"
    assert hour_log.min_power == min_power, "min power is the same"
    assert hour_log.max_power == max_power, "max power is the same"
