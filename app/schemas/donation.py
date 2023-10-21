"""
Pydantic схемы модели Donation.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreateBase(BaseModel):
    """
    Создание пожертвования и базовый класс для других схем.
    """
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationGet(DonationCreateBase):
    """
    Краткая информация о пожертвовании из БД.
    """
    id: int
    create_date: datetime

    class Config: # noqa
        orm_mode = True


# todo объединить со схемой проекта и сделать базовую схему
class DonationGetAll(DonationGet):
    """
    Инфо о всех пожертвованиях пользователя.
    """
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config: # noqa
        orm_mode = True
