"""Sensor API tests"""

import pytest
from flask import json

def test_sensor_post_empty(flask_client, create_space):
    """Test an API call to post empty sensor data"""
    result = flask_client.post('/sensor_api/v1/', json=dict(
        temperature=19.3,
        humidity=58.3,
        power=523.23,
        space_id=1,
    ))

    data = result.get_json()
    assert 'temperature' in data
    assert isinstance(data['temperature'], str), "Result temperature should be a string"
    assert 'humidity' in data
    assert isinstance(data['humidity'], str), "Result humidity should be a string"
    assert 'power' in data
    assert isinstance(data['power'], str), "Result power should be a string"
    assert 'space_id' in data
    assert isinstance(data['space_id'], int), "Result space_id should be an int"
