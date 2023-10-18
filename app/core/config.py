"""
Конфигурация приложения.
"""
from pydantic import BaseSettings


class Settings(BaseSettings): # noqa
    db_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    # todo нужна?
    path: str
    app_title: str = 'QRKot'
    app_description: str = ('Приложение для Благотворительного фонда '
                            'поддержки котиков QRKot')
    secret: str = 'secret'

    class Config: # noqa
        env_file = '.env'


settings = Settings()
