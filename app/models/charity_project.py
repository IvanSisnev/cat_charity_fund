"""
Модель благотворительных проектов.
"""
from sqlalchemy import Column, String, Text

from app.models.basemodel import BaseModel


class CharityProject(BaseModel): # noqa
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'Благотворительный проект. Внесено: {super().__repr__()}'
