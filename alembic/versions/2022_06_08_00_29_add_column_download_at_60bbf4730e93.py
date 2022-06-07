"""add column download_at

Revision ID: 60bbf4730e93
Revises: 80354063b9f5
Create Date: 2022-06-08 00:29:55.564027

"""
from alembic.op import add_column, drop_column
from sqlalchemy import Column, DateTime


# revision identifiers, used by Alembic.
revision = '60bbf4730e93'
down_revision = '80354063b9f5'
branch_labels = None
depends_on = None


def upgrade():
    add_column('source', Column('download_at', DateTime, nullable=False))


def downgrade():
    drop_column('source', 'download_at')
