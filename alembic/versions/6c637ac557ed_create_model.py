"""create model

Revision ID: 6c637ac557ed
Revises: 
Create Date: 2022-06-05 10:19:40.355374

"""
from datetime import datetime

from alembic.op import create_table, drop_table
from sqlalchemy import Column, Integer, String, DateTime


revision = '6c637ac557ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    create_table(
        'news',
        Column('id', Integer, nullable=False, autoincrement=True, primary_key=True),
        Column('news_label', String),
        Column('news_url', String),
        Column('data', String),
        Column('created_at', DateTime, nullable=False, default=datetime.now()),
        Column('updated_at', DateTime),
    )


def downgrade():
    drop_table('news')
