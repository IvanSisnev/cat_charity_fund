"""
Модель благотворительных проектов.
"""
from sqlalchemy import Column, String, Text

from basemodel import AbstractBase


class CharityProject(AbstractBase): # noqa
    name = Column(String(100), nullable=False)
    # todo 1 символ?
    description = Column(Text(1), nullable=False)

    def __repr__(self):
        return f'Благотворительный проект. Внесено: {super().__repr__()}'
