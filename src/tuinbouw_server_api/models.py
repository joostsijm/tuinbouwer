"""Models"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Space(db.Model):
    """Model for space"""
    id = db.Column(db.Integer, primary_key=True)
