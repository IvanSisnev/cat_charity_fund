"""
CRUD операции модели CharityProject.
"""
from app.crud.base import BaseCRUD
from app.models.charityproject import CharityProject


class CharityProjectCRUD(BaseCRUD):
    """
    CRUD операции модели CharityProject.
    """
    pass


charity_project_crud = CharityProjectCRUD(CharityProject)
