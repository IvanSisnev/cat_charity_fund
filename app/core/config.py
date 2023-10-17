"""
Конфигурация приложения.
"""
from pydantic import BaseSettings


class Settings(BaseSettings): # noqa
    db_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    # todo нужна?
    path: str
    app_title: str
    app_description: str

    class Config: # noqa
        env_file = '.env'


settings = Settings()
