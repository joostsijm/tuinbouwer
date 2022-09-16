"""Test configuration"""

import os
import tempfile

import pytest
from dotenv import load_dotenv
import flask_migrate

from tuinbouwer_server_api import create_app, models


load_dotenv()

@pytest.fixture()
def flask_client():
    """Initialize Flask application for testing"""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////' + db_path + '.sqlite',
        # 'SQLALCHEMY_DATABASE_URI': 'postgresql://tuinbouwer@localhost/tuinbouwer_test',
    })

    with app.test_client() as client:
        with app.app_context():
            # flask_migrate.upgrade()
            models.db.create_all()
            yield client

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture()
def create_space(flask_client):
    """Create space in database"""
    space = models.Space()
    space.name = 'test space'
    models.db.session.add(space)
    models.db.session.commit()
