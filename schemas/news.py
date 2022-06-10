"""Pydantic схемы"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, AnyUrl, PositiveInt, validator

from const.const import SourceTypeEnum


class SourceSchemaRequest(BaseModel):
    """Модель для добавления нового источника"""

    news_label: str = Field(alias='news_label')
    news_url: AnyUrl = Field(alias='news_url')
    interval_sec: PositiveInt = Field(alias='interval_sec')
    source_type: SourceTypeEnum = Field(alias='source_type')


class SourceSchemaResponse(BaseModel):
    """Модель для формирования ответа со списком источников новостей"""

    id: int
    news_label: str
    news_url: AnyUrl
    interval_sec: PositiveInt
    source_type: SourceTypeEnum


class NewsSchema(BaseModel):
    """Модель для добавления нового источника"""

    source_id: int
    data: str


class HTTPQuerySchema(BaseModel):
    """Схема запроса номера страницы и размера страницы"""

    page: PositiveInt = 1
    page_size: PositiveInt = 10


class RSSArticleSchema(BaseModel):
    """Схема RSS статьи"""

    author: Optional[str] = ''
    title: Optional[str] = ''
    link: Optional[str] = ''
    description: Optional[str] = ''
    pub_date: datetime = Field(alias='pubDate')
    category: Optional[str] = ''

    @validator("author", pre=True)
    def parse_author(cls, value):
        return value if value else ''

    @validator("title", pre=True)
    def parse_title(cls, value):
        return value if value else ''

    @validator("link", pre=True)
    def parse_link(cls, value):
        return value if value else ''

    @validator("category", pre=True)
    def parse_category(cls, value):
        return value if value else ''

    @validator("pub_date", pre=True)
    def parse_pub_date(cls, value):
        if isinstance(value, str):
            result = datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z")
        else:
            result = value
        return result

    def __hash__(self):
        return hash(str(self.author) + str(self.title) + str(self.link) + str(self.pub_date))

    def __eq__(self, other):
        result = self.author == other.author
        result &= self.title == other.title
        result &= self.link == other.link
        result &= self.pub_date == other.pub_date
        return result
