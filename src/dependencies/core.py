from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session_stub
from repositories.core import CoreRepository
from services.core import CoreService


def get_core_service(session: Annotated[AsyncSession, Depends(get_session_stub)]):
    return CoreService(repo=CoreRepository(session))
