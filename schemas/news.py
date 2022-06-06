"""Модуль содержит модель сайта"""

from pydantic import BaseModel, Field, AnyUrl, PositiveInt

from const.const import SourceTypeEnum


class SourceSchema(BaseModel):
    """Модель для добавления нового источника"""

    news_label: str = Field(alias='news_label')
    news_url: AnyUrl = Field(alias='news_url')
    interval_sec: PositiveInt = Field(alias='interval_sec')
    source_type: SourceTypeEnum = Field(alias='source_type')


class SourceSchemaInDB(SourceSchema):
    id: int
    #
    # class Config:
    #     """Конфигурация"""
    #
    #     orm_mode = True
