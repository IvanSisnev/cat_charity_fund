"""
Эндпоинты пожертвований.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectRead,
                                        CharityProjectUpdate)

router = APIRouter()
