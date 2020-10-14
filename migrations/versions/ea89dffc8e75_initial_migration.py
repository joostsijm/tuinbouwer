"""initial_migration

Revision ID: ea89dffc8e75
Revises: 
Create Date: 2020-10-09 15:15:00.278533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea89dffc8e75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('space',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('space')
