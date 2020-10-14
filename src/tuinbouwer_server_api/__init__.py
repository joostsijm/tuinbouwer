"""Flask application"""

import os

from flask import Flask
from dotenv import load_dotenv

from tuinbouwer_server_api  import sensor_api


load_dotenv()

def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI='sqlite:////' + os.path.join(app.instance_path, 'app.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database models
    from tuinbouwer_server_api.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(sensor_api.sensor_api)

    return app
