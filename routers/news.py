from typing import List

from fastapi import APIRouter, Depends

from crud.news import SourceCRUD, NewsCRUD
from schemas.news import SourceSchemaRequest, SourceSchemaResponse, HTTPQuerySchema
from utils.news_parser import ParserFabric

router = APIRouter(prefix="/api/v1/sources", tags=["Импорт новостей"])


@router.post("/")
async def add_source(source_schema: SourceSchemaRequest) -> dict:
    """
    Добавление нового источника новостей
    :param source_schema:
    :return:
    """
    source_crud = SourceCRUD()
    new_source = await source_crud.create(object_in=source_schema)
    return new_source


@router.get("/", response_model=List[SourceSchemaResponse])
async def list_sources(http_query: HTTPQuerySchema = Depends()) -> dict:
    """
    Отображение списка источников новостей
    """
    source_crud = SourceCRUD()
    sources = await source_crud.select_sources(http_query=http_query)
    return sources


@router.get("/{source_id}/news", response_model=List[dict])
async def list_sources(source_id: int, http_query: HTTPQuerySchema = Depends()) -> dict:
    """
    Отображение списка источников новостей
    """
    parsed_news = []
    news_crud = NewsCRUD()
    news_models = await news_crud.select_news(source_id=source_id, http_query=http_query)
    if news_models:
        source = news_models[0][0].source
        parser_cls = ParserFabric().get_parser(source_type=source.source_type)
        if parser_cls:
            parsed_news = parser_cls(news_models=news_models, http_query=http_query).parse()
    return parsed_news
