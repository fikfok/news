"""
Предоставляет класс Settings, который забирает из .env-файла настройки
"""

import functools

import pydantic


class Settings(pydantic.BaseSettings):
    """Класс для хранения(получения) настроек приложения."""
    db_username: str
    db_password: str
    db_database: str
    db_host: str
    db_port: str

    postgresql_pool_connections: int = 50
    postgresql_max_overflow: int = 50
    postgresql_pool_recycle: int = 180
    postgresql_log: bool = True

    @property
    def postgresql_url_async(self) -> str:
        """Метод собирает строку для запроса к postgesql в асинхронном режиме."""
        url: str = (
            f'postgresql+asyncpg://{self.db_username}:{self.db_password}@'
            f'{self.db_host}:{self.db_port}/{self.db_database}'
        )

        return url

    class Config:
        """Класс конфигурации для указания пути к '.env'."""
        env_file = '.env'


@functools.lru_cache()
def get_settings() -> Settings:
    """Кеш для предотвращения пересоздания экземпляра Settings."""
    return Settings()


settings = get_settings()
