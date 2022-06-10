"""Модуль с задачами для запуска в фоне при помощи celery"""
import asyncio
from datetime import datetime

from celery import Celery
from celery.schedules import crontab
from loguru import logger

from crud.news import SourceCRUD
from news.config import settings
from utils.news_downloader import NewsDownloader

celery = Celery(
    __name__,
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)


def handle_exception(loop, context):
    """Обработчик исключений возникцих в цикле событий."""

    logger.error(context)


# Создаем новый цикл событий.
event_loop = asyncio.new_event_loop()
# Устанавливаем обработчик исключений возникших в цикле событий.
event_loop.set_exception_handler(handle_exception)


GET_NEWS_TASK = 'news_task'


@celery.task(name=GET_NEWS_TASK)
def news_task() -> bool:
    """Celery таска, которая запрашивает очередную порцию новостей из источников"""
    crud = SourceCRUD()
    results, _ = event_loop.run_until_complete(asyncio.wait([crud.select_sources_for_download()]))
    sources = list(results)[0].result()

    logger.debug(f'Sources count: {len(sources)}')

    news_downloader = NewsDownloader(sources=sources)
    event_loop.run_until_complete(news_downloader.process())
    return True


# Периодический запуск обработки таблиц
celery.conf.beat_schedule = {
    # Запускаем задачи по запросу статистики.
    GET_NEWS_TASK: {
        'task': GET_NEWS_TASK,
        'schedule': crontab(minute='*/1'),
    },
}
