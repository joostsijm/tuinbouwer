"""Models"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Space(db.Model):
    """Model for space"""
    id = db.Column(db.Integer, primary_key=True)
