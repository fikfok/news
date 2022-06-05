"""Настройка подключения к базе данных."""
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

from news.config import settings


async_engine = create_async_engine(
    settings.postgresql_url_async,
    future=True,
    echo=settings.postgresql_log,
    pool_size=settings.postgresql_pool_connections,
    max_overflow=settings.postgresql_max_overflow,
    pool_recycle=settings.postgresql_pool_recycle,
    poolclass=AsyncAdaptedQueuePool,
)

async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
)

Base: Any = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение текущей сессии"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

db_session = asynccontextmanager(get_db)
