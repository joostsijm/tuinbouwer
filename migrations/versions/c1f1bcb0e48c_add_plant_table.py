"""add_plant_table

Revision ID: c1f1bcb0e48c
Revises: ea89dffc8e75
Create Date: 2020-10-09 16:15:40.062923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1f1bcb0e48c'
down_revision = 'ea89dffc8e75'
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
    op.add_column('space', sa.Column('name', sa.String(), nullable=True))


def downgrade():
    op.drop_column('space', 'name')
    op.drop_table('plant')
