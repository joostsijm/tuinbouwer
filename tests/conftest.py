"""Test configuration"""

import os

import pytest
from dotenv import load_dotenv

from tuinbouw_server_api import create_app

load_dotenv()

@pytest.fixture(scope="module")
def flask():
    """Run Flask before test"""
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
