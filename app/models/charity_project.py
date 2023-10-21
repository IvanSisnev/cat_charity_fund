"""
Модель благотворительных проектов.
"""
from sqlalchemy import Column, String, Text

from app.models.basemodel import BaseModel


class CharityProject(BaseModel):
    """
    Унаследовать общие поля, дописать уникальные поля для модели
    благотворительного проекта.
    """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
