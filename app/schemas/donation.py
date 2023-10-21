"""
Pydantic схемы модели Donation.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreateBase(BaseModel):
    """
    Создать пожертвование. Наследуемый базовый класс.
    """
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationGet(DonationCreateBase):
    """
    Наследовать поля. Получить информацию о пожертвовании из БД.
    """
    id: int
    create_date: datetime

    class Config: # noqa
        orm_mode = True


class DonationGetAll(DonationGet):
    """
    Наследовать поля. Получить информацию о всех пожертвованиях пользователя.
    """
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config: # noqa
        orm_mode = True
