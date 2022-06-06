from fastapi import APIRouter

from crud.news import SourceCRUD
from models.news import Source
from schemas.news import SourceSchema, SourceSchemaInDB

router = APIRouter(prefix="/api/v1/news", tags=["Импорт новостей"])


@router.post("/")
async def news(source_schema: SourceSchema) -> SourceSchemaInDB:
    source_entity = SourceCRUD()
    new_source = await source_entity.create(object_in=source_schema)
    return new_source
