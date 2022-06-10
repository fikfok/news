"""Загрузчик новостей из источника"""
from typing import List, Dict

import aiohttp

from crud.news import NewsCRUD, SourceCRUD
from models.news import Source
from news.database import db_session
from schemas.news import NewsSchema


class NewsDownloader:
    def __init__(self, sources: List[Source]):
        self._sources = sources

    async def process(self):
        """Производит обработку адресов по списку источников"""

        for source in self._sources:
            await self._process_single_source(source_id=source.id, source_url=source.news_url)

    async def _process_single_source(self, source_id: int, source_url: str):
        """
        Производит обработку адресов из конкретного источника:
            1. запрашивает блок новости по URL'у;
            2. сохраняет блок новостей в БД;
            3. источнику новостей обновляет следующую дату и время загрузки.
        """

        # 1. Запросить блок новостей по URL'у
        raw_news = await self._download_news(source_url=source_url)

        async with db_session() as session:
            # 2. Сохранить в БД
            news_schema = NewsSchema(source_id=source_id, data=raw_news)
            news_crud = NewsCRUD(session=session)
            await news_crud.create(object_in=news_schema)

            # 3. Источнику новостей вычислить следующую дату и время загрузки и сохранить.
            source_crud = SourceCRUD(session=session)
            await source_crud.update_next_download_dt(source_id=source_id)

            await session.commit()

    async def _download_news(self, source_url: str) -> str:
        """Запрашивает новости из конкретного источника"""

        async with aiohttp.ClientSession() as session:
            async with session.get(source_url) as resp:
                # resp_stat = resp.status
                resp_text = await resp.text()
        return resp_text
