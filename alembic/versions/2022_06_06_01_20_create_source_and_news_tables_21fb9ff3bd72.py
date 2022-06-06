"""create source and news tables

Revision ID: 21fb9ff3bd72
Revises: 6c637ac557ed
Create Date: 2022-06-06 01:20:42.057648

"""
from datetime import datetime

from alembic.op import create_table, drop_table
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, PrimaryKeyConstraint, text, func, \
    DefaultClause

# revision identifiers, used by Alembic.
revision = '21fb9ff3bd72'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    create_table(
        'source',
        Column('id', Integer, nullable=False, autoincrement=True, primary_key=True),
        Column('news_label', String),
        Column('news_url', String, unique=True),
        Column('interval_sec', Integer),
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        PrimaryKeyConstraint('id', name='source_pkey'),
    )
    create_table(
        'news',
        Column('id', Integer, nullable=False, autoincrement=True, primary_key=True),
        Column('source_id', Integer),
        Column('data', String),
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        PrimaryKeyConstraint('id', name='news_pkey'),
        ForeignKeyConstraint(('source_id',), ['source.id'], name='source_id_source_fkey', ondelete='CASCADE'),
    )


def downgrade():
    drop_table('source')
    drop_table('news')
