"""add content column to posts table

Revision ID: dc0c1215d315
Revises: fe4648bfb840
Create Date: 2024-04-15 13:44:39.670317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc0c1215d315'
down_revision = 'fe4648bfb840'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
