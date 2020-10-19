"""add_date_time_in_sensor_log

Revision ID: 0315a2a66fa9
Revises: f55c254c3edd
Create Date: 2020-10-19 11:00:14.505944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0315a2a66fa9'
down_revision = 'f55c254c3edd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sensor_log', sa.Column('date_time', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('sensor_log', 'date_time')
