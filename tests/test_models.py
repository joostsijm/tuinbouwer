"""Models tests"""

from decimal import Decimal

from tuinbouwer_server_api import models


def test_space_add(flask_client):
    """Test adding space to database"""
    space = models.Space()
    space.name = 'test space'
    models.db.session.add(space)
    models.db.session.commit()
    assert isinstance(space.id, int), "The id should be an int"
    assert isinstance(space.name, str), "The name should be a str"
    assert space.name == 'test space', "The name should be 'test space'"

def test_plant_add(flask_client):
    """Test adding plant to database"""
    plant = models.Plant()
    plant.name = 'test plant'
    plant.harvest = 1
    plant.number = 1
    models.db.session.add(plant)
    models.db.session.commit()
    assert isinstance(plant.id, int), "The id should be an int"
    assert isinstance(plant.name, str), "The name should be a str"
    assert isinstance(plant.harvest, int), "The harvest should be an int"
    assert isinstance(plant.number, int), "The number should be an int"
    assert plant.name == 'test plant', "The name should 'test plant'"

def test_sensor_log_add(flask_client):
    """Test adding sensor log to database"""
    sensor_log = models.SensorLog()
    sensor_log.temperature = 19.3
    sensor_log.humidity = 30
    sensor_log.power = 353.34
    sensor_log.space_id = 1
    models.db.session.add(sensor_log)
    models.db.session.commit()
    assert isinstance(sensor_log.id, int), "Sensor log id should be an int"
    assert isinstance(sensor_log.temperature, Decimal), "Sensor log temperature should be an int"
    assert isinstance(sensor_log.humidity, Decimal), "Sensor log humidity should be an int"
    assert isinstance(sensor_log.power, Decimal), "Sensor log power should be an int"
