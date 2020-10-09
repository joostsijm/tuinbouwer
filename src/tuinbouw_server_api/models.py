"""Models"""

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

meta = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
})
db = SQLAlchemy(metadata=meta)
migrate = Migrate()

plants = db.Table('plants',
    db.Column('space_id', db.Integer, db.ForeignKey('space.id'), primary_key=True),
    db.Column('plant_id', db.Integer, db.ForeignKey('plant.id'), primary_key=True),
    db.Column('move_date', db.Date, nullable=False),
)

class Space(db.Model):
    """Model for space"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    plants = db.relationship('Plant', secondary=plants, lazy='subquery',
        backref=db.backref('pages', lazy=True))


class Plant(db.Model):
    """Model for plant"""
    id = db.Column(db.Integer, primary_key=True)
    # Self made name for the plant
    name = db.Column(db.String)
    # Plant specie
    specie = db.Column(db.String)
    # Harvest iteration
    harvest = db.Column(db.Integer, nullable=False)
    # Number of plant in the harvest
    number = db.Column(db.SmallInteger, nullable=False)
    # Date of the germination
    germination_date = db.Column(db.Date)
    # Date of the first signs of bloom
    bloom_date = db.Column(db.Date)
    # harvest date
    harvest_date = db.Column(db.Date)
    # Yield of the harvest
    yield_ = db.Column('yield', db.Integer)


class SensorLog(db.Model):
    """Model for sensor log"""
    id = db.Column(db.Integer, primary_key=True)
    # Temperature in celcius
    temperature = db.Column(db.DECIMAL(3, 1))
    # Air humidity
    humidity = db.Column(db.SmallInteger)
    # Power in watts
    power = db.Column(db.DECIMAL(6, 2))
