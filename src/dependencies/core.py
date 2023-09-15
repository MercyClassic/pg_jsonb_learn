from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from repositories.core import CoreRepository
from services.core import CoreService


def get_core_service(session: AsyncSession = Depends(get_async_session)):
    return CoreService(repo=CoreRepository(session))
