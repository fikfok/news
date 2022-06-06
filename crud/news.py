from typing import TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import func, literal_column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base

from models.news import Source
from news.database import db_session
from schemas.news import SourceSchema


Base = declarative_base()

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class BaseCRUD:
    """Базовый класс дял работы с моделями"""
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, object_in: CreateSchemaType):
        """Создание источника новостей"""

        async with db_session() as session:
            entity_data = object_in.dict()
            stmt = (insert(self.model).
                    values(**entity_data).
                    on_conflict_do_update(index_elements=['news_url'], set_={**entity_data, 'updated_at': func.now()}).
                    returning(self.model))

            result = (await session.execute(stmt)).scalar_one_or_none()
            await session.commit()
        return {'id': result, **entity_data}


class SourceCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(model=Source)
