"""
Модель пожертвований.
"""
from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.basemodel import BaseModel


class Donation(BaseModel):
    """
    Унаследовать общие поля, дописать уникальные поля для модели
    пожертвования.
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
