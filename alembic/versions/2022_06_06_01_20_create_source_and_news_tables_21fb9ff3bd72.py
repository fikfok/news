"""create source and news tables

Revision ID: 21fb9ff3bd72
Revises: 6c637ac557ed
Create Date: 2022-06-06 01:20:42.057648

"""
from datetime import datetime

from alembic.op import create_table, drop_table
from sqlalchemy import Column, Integer, String, DateTime


# revision identifiers, used by Alembic.
revision = '21fb9ff3bd72'
down_revision = '6c637ac557ed'
branch_labels = None
depends_on = None


def upgrade():
    create_table(
        'source',
        Column('id', Integer, nullable=False, autoincrement=True, primary_key=True),
        Column('news_label', String),
        Column('news_url', String),
        Column('interval_sec', Integer),
        Column('created_at', DateTime, nullable=False, default=datetime.now()),
        Column('updated_at', DateTime),
    )


def downgrade():
    drop_table('source')
    drop_table('news')
