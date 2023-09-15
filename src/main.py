import logging
from logging import config

from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from config import LOGGING_CONFIG
from routers.core import router as core_router

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


app = FastAPI(title='postgresql_json_learn')


@app.exception_handler(Exception)
async def unexpected_error_log(request, ex):
    logger.error(ex)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=None)


app.include_router(core_router)
