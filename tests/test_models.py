"""Models tests"""

import pytest

from tuinbouw_server_api import models

def test_space_add(flask):
    """Test adding empty space to database"""
    space = models.Space()
    space.name = "test space"

    models.db.session.add(space)
    models.db.session.commit()

    assert isinstance(space.id, int), "The id should be an int"
    assert isinstance(space.name, str), "The name should be a str"

def test_plant_add(flask):
    """Test adding empty space to database"""
    space = models.Space()
    space.name = "test space"

    models.db.session.add(space)
    models.db.session.commit()

    assert isinstance(space.id, int), "The id should be an int"
    assert isinstance(space.name, str), "The name should be a str"
