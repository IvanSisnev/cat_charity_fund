"""
Pydantic схемы модели CharityProject.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    """
    Базовый класс для схем.
    """
    class Config: # noqa
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    """
    Создание проекта.
    """
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """
    Изменение проекта.
    """
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    full_amount: Optional[PositiveInt]


class CharityProjectRead(BaseModel):
    """
    Инфо о проекте из БД.
    """
    name: str
    description: str
    full_amount: PositiveInt
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config: # noqa
        orm_mode = True
