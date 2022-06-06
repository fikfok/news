"""Описание моделей для таблиц базы данных"""
from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship

from news.database import Base


class Source(Base):
    """Описание полей для таблицы Source"""

    __tablename__ = 'source'

    id = Column(Integer, primary_key=True, autoincrement=True)
    news_label = Column(String)
    news_url = Column(String, unique=True)
    interval_sec = Column(Integer)
    news = relationship('News', cascade='all,delete', back_populates='source')
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)


class News(Base):
    """Описание полей для таблицы News"""

    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey('source.id', ondelete='CASCADE'), nullable=False)
    source = relationship('Source', cascade='all,delete', back_populates='sources')
    data = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
