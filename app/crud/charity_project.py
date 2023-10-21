"""
CRUD операции модели CharityProject.
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models.charity_project import CharityProject


class CharityProjectCRUD(BaseCRUD):
    """
    CRUD операции модели CharityProject.
    """
    async def get_id_by_name(self, charity_project_name: str, # noqa
                             session: AsyncSession) -> Optional[int]:
        """
        Ищет в БД проекты с таким же названием.
        """
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return charity_project_id.scalars().first()


charity_project_crud = CharityProjectCRUD(CharityProject)
