"""Test configuration"""

import os
import tempfile

import pytest
from dotenv import load_dotenv

from tuinbouw_server_api import create_app

load_dotenv()

@pytest.fixture(scope="module")
def flask():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    with app.app_context():
        app.db.init_db()
    yield app

    os.close(db_fd)
    os.unlink(db_path)
