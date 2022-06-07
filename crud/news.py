from datetime import datetime, timedelta
from typing import TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base

from models.news import Source
from news.database import db_session


Base = declarative_base()

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class BaseCRUD:
    """Базовый класс дял работы с моделями"""
    def __init__(self, model: Type[ModelType]):
        self.model = model


class SourceCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(model=Source)

    async def create(self, object_in: CreateSchemaType) -> dict:
        """Создание источника новостей"""

        async with db_session() as session:
            entity_data = object_in.dict()
            entity_data['download_at'] = datetime.now() + timedelta(seconds=entity_data['interval_sec'])
            stmt = (insert(self.model).
                    values(**entity_data).
                    on_conflict_do_update(index_elements=['news_url'], set_={**entity_data, 'updated_at': func.now()}).
                    returning(self.model))

            result = (await session.execute(stmt)).scalar_one_or_none()
            await session.commit()
        return {'id': result, **entity_data}

    async def select_sources_for_download(self):
        """Извлечь все источники новостей, для которых подошло время загрузки новостей"""

        async with db_session() as session:
            stmt = select(self.model).where(self.model.download_at < datetime.now())
            result = await session.execute(stmt)
        sources_for_download = result.fetchall()
        return [row[0] for row in sources_for_download]
