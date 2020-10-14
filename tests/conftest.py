"""Test configuration"""

import os
import tempfile

import pytest
from dotenv import load_dotenv
import flask_migrate

from tuinbouwer_server_api import create_app

load_dotenv()

@pytest.fixture(scope="module")
def flask():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////' + db_path + '.sqlite',
    })
    with app.app_context():
        flask_migrate.upgrade()
        yield app

    os.close(db_fd)
    os.unlink(db_path)
