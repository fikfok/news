"""source_type

Revision ID: 80354063b9f5
Revises: 21fb9ff3bd72
Create Date: 2022-06-06 17:20:58.360310

"""
from alembic.op import add_column, drop_column, get_bind
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM

from const.const import SourceTypeEnum

revision = '80354063b9f5'
down_revision = '21fb9ff3bd72'
branch_labels = None
depends_on = None


def upgrade():
    source_type = ENUM(SourceTypeEnum, name='source_type')
    source_type.create(get_bind(), checkfirst=True)
    add_column('source', Column('source_type', source_type))


def downgrade():
    source_type = ENUM(SourceTypeEnum, name='source_type')
    source_type.drop(get_bind())
