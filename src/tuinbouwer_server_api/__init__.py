"""Flask application"""

import os
import decimal

from flask import Flask, json
from dotenv import load_dotenv
from flask_cors import CORS
import openai

from tuinbouwer_server_api.blueprints import website, api

load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder"""

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(JSONEncoder, self).default(obj)


def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('FLASK_SQLALCHEMY_DATABASE_URI'),
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

    # Set custom json encoder
    app.json_encoder = JSONEncoder

    # SQLAlchemy
    from tuinbouwer_server_api.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Apscheduler
    from tuinbouwer_server_api.scheduler import scheduler, start_jobs
    scheduler.init_app(app)
    scheduler.start()
    start_jobs()

    # CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # Website
    app.register_blueprint(website.frontend.blueprint)

    # API
    app.register_blueprint(api.sensor.blueprint)
    app.register_blueprint(api.frontend.blueprint)

    return app
