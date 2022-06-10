from datetime import datetime
from typing import TypeVar, Type, Optional

from pydantic import BaseModel
from sqlalchemy import func, update, text, cast, String, bindparam, Interval
from sqlalchemy.dialects.postgresql import insert, INTERVAL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, joinedload
import sqlalchemy.sql.expression as sorting
from sqlalchemy.sql import Select
from sqlalchemy.sql.functions import concat
import xmltodict

from models.news import Source, News
from news.database import db_session
from schemas.news import HTTPQuerySchema


Base = declarative_base()

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class BaseCRUD:
    """Базовый класс дял работы с моделями"""
    def __init__(self, model: Type[ModelType], session: Optional[AsyncSession] = None):
        self._model = model
        self._session = session

    async def _execute_stmt(self, stmt):
        """

        :param stmt:
        :return:
        """
        if self._session:
            await self._session.execute(stmt)
        else:
            async with db_session() as session:
                await session.execute(stmt)
                await session.commit()

    def _apply_pagination(self, stmt: Select, http_query: HTTPQuerySchema) -> Select:
        """Применить пагинацию"""
        skip = http_query.page_size * (http_query.page - 1)
        new_stmt = stmt.offset(skip).limit(http_query.page_size)
        return new_stmt


class NewsCRUD(BaseCRUD):
    def __init__(self, **kwargs):
        super().__init__(model=News, **kwargs)

    async def create(self, object_in: CreateSchemaType) -> None:
        """
        Вставка блока новостей

        """
        entity_data = object_in.dict()
        stmt = insert(self._model).values(**entity_data)
        await self._execute_stmt(stmt=stmt)

    async def select_news(self, source_id: int, http_query: HTTPQuerySchema):
        """ """
        async with db_session() as session:
            stmt = (select(self._model).
                    options(joinedload(self._model.source)).
                    where(self._model.source_id == source_id).
                    order_by(sorting.asc(self._model.id)))
            result = await session.execute(stmt)
            news = result.fetchall()
        return news


class SourceCRUD(BaseCRUD):
    def __init__(self, **kwargs):
        super().__init__(model=Source, **kwargs)

    async def create(self, object_in: CreateSchemaType) -> dict:
        """
        Создание источника новостей

        """

        async with db_session() as session:
            entity_data = object_in.dict()
            entity_data['download_at'] = datetime.now()
            stmt = (insert(self._model).
                    values(**entity_data).
                    on_conflict_do_update(index_elements=['news_url'], set_={**entity_data, 'updated_at': func.now()}).
                    returning(self._model))

            result = (await session.execute(stmt)).scalar_one_or_none()
            await session.commit()
        return {'id': result, **entity_data}

    async def select_sources_for_download(self):
        """Извлечь все источники новостей, для которых подошло время загрузки новостей"""

        async with db_session() as session:
            stmt = select(self._model).where(self._model.download_at < datetime.now())
            result = await session.execute(stmt)
            sources_for_download = result.fetchall()
        return [row[0] for row in sources_for_download]

    async def calc_next_download_dt(self, source_id: int) -> None:
        """

        :param source_id:
        :return:
        """
        stmt = (update(self._model).
                where(self._model.id == source_id).
                values(download_at=func.now() + func.cast(concat(self._model.interval_sec, ' seconds'), INTERVAL)))
        await self._execute_stmt(stmt=stmt)

    async def select_sources(self, http_query: HTTPQuerySchema):
        """Извлечь все источники новостей по условию"""

        async with db_session() as session:
            stmt = select(self._model).order_by(sorting.asc(self._model.news_label))
            stmt = self._apply_pagination(stmt=stmt, http_query=http_query)
            result = await session.execute(stmt)
            sources = result.fetchall()
        result = [row[0].__dict__ for row in sources]
        return result

