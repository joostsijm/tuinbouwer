"""Test configuration"""

import os
import tempfile

import pytest
from dotenv import load_dotenv
import flask_migrate

from tuinbouwer_server_api import create_app, models


load_dotenv()

@pytest.fixture()
def client():
    """Initialize Flask application for testing"""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////' + db_path + '.sqlite',
    })

    with app.test_client() as client:
        with app.app_context():
            flask_migrate.upgrade()
            space = models.Space()
            space.name = 'test space'
            models.db.session.add(space)
            models.db.session.commit()
        yield client

    os.close(db_fd)
    os.unlink(db_path)
