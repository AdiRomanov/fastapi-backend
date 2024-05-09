"""Add recipe table

Revision ID: 172a637c47e8
Revises: 2ad2d886faf4
Create Date: 2024-05-09 13:40:10.995170

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB



# revision identifiers, used by Alembic.
revision = '172a637c47e8'
down_revision = '2ad2d886faf4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('cook_time', sa.Integer(), nullable=False),
    sa.Column('ingredients', JSONB, nullable=False),
    sa.Column('directions', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('recipes')
