import logging
from logging import config

from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from config import LOGGING_CONFIG
from db.database import get_async_session, get_session_stub
from routers.core import router as core_router

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


app = FastAPI(title='postgresql_json_learn')

app.dependency_overrides[get_session_stub] = get_async_session


@app.exception_handler(Exception)
async def unexpected_error_log(request, ex):
    logger.error(ex)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=None)


app.include_router(core_router)
