from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import WebConfig
from db.database import get_session_stub
from dependencies.stub import Stub
from repositories.core import CoreRepository
from services.core import CoreService


def get_core_service(
    session: Annotated[AsyncSession, Depends(get_session_stub)],
    config: Annotated[WebConfig, Depends(Stub(WebConfig))],
):
    return CoreService(
        CoreRepository(session),
        config.media_dir,
    )
