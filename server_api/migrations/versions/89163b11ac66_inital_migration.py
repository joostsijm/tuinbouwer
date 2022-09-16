"""inital_migration

Revision ID: 89163b11ac66
Revises: 
Create Date: 2020-10-16 07:45:24.000669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89163b11ac66'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('plant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('specie', sa.String(), nullable=True),
    sa.Column('harvest', sa.Integer(), nullable=False),
    sa.Column('number', sa.SmallInteger(), nullable=False),
    sa.Column('germination_date', sa.Date(), nullable=True),
    sa.Column('bloom_date', sa.Date(), nullable=True),
    sa.Column('harvest_date', sa.Date(), nullable=True),
    sa.Column('yield', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_plant'))
    )
    op.create_table('space',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_space'))
    )
    op.create_table('plants',
    sa.Column('space_id', sa.Integer(), nullable=False),
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.Column('move_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['plant_id'], ['plant.id'], name=op.f('fk_plants_plant_id_plant')),
    sa.ForeignKeyConstraint(['space_id'], ['space.id'], name=op.f('fk_plants_space_id_space')),
    sa.PrimaryKeyConstraint('space_id', 'plant_id', name=op.f('pk_plants'))
    )
    op.create_table('sensor_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.DECIMAL(precision=3, scale=1), nullable=False),
    sa.Column('humidity', sa.DECIMAL(precision=3, scale=1), nullable=False),
    sa.Column('power', sa.DECIMAL(precision=6, scale=2), nullable=False),
    sa.Column('space_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['space_id'], ['space.id'], name=op.f('fk_sensor_log_space_id_space')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sensor_log'))
    )


def downgrade():
    op.drop_table('sensor_log')
    op.drop_table('plants')
    op.drop_table('space')
    op.drop_table('plant')
