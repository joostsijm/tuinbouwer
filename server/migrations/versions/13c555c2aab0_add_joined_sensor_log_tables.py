"""add_joined_sensor_log_tables

Revision ID: 13c555c2aab0
Revises: 89163b11ac66
Create Date: 2020-10-16 16:06:25.687839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13c555c2aab0'
down_revision = '89163b11ac66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('day_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['sensor_log.id'], name=op.f('fk_day_log_id_sensor_log')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_day_log'))
    )
    op.create_table('hour_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hour', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['sensor_log.id'], name=op.f('fk_hour_log_id_sensor_log')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_hour_log'))
    )
    op.create_table('minute_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('minute', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['sensor_log.id'], name=op.f('fk_minute_log_id_sensor_log')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_minute_log'))
    )
    op.create_table('month_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('month', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['sensor_log.id'], name=op.f('fk_month_log_id_sensor_log')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_month_log'))
    )
    op.create_table('week_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['sensor_log.id'], name=op.f('fk_week_log_id_sensor_log')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_week_log'))
    )
    op.add_column('sensor_log', sa.Column('log_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sensor_log', 'log_type')
    op.drop_table('week_log')
    op.drop_table('month_log')
    op.drop_table('minute_log')
    op.drop_table('hour_log')
    op.drop_table('day_log')
    # ### end Alembic commands ###