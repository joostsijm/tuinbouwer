"""add_sensor_log_table

Revision ID: 037af9b501ce
Revises: 97beb28bd6c3
Create Date: 2020-10-09 19:23:59.661309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '037af9b501ce'
down_revision = '97beb28bd6c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('sensor_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.DECIMAL(precision=3, scale=1), nullable=False),
    sa.Column('humidity', sa.DECIMAL(precision=3, scale=1), nullable=False),
    sa.Column('power', sa.DECIMAL(precision=6, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sensor_log'))
    )


def downgrade():
    op.drop_table('sensor_log')
