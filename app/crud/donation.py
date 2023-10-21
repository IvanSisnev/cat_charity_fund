"""
CRUD операции модели Donation.
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models import Donation, User


class DonationProjectCRUD(BaseCRUD):
    """
    CRUD операции модели Donation.
    """
    async def get_users_donations( # noqa
            self, user: User, session: AsyncSession
    ) -> list[Optional[Donation]]:
        """
        Получить из БД все пожертвования пользователя.
        """
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return user_donations.scalars().all()


donation_crud = DonationProjectCRUD(Donation)
