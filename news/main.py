from fastapi import FastAPI

from news.config import get_settings
from news.openapi import tags_metadata
from routers import news


app = FastAPI(
    title='News microservice',
    openapi_tags=tags_metadata,
    docs_url='/docs',
)
app_settings = get_settings()

app.include_router(news.router)
