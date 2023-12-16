import logging
import os
from logging import config
from pathlib import Path

from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from config import get_logging_dict
from dependencies.di.init_dependencies import init_dependencies
from routers.core import router as core_router

root_dir = '%s' % Path(__file__).parent

config.dictConfig(get_logging_dict(root_dir))
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title='postgresql_json_learn')
    init_dependencies(app, os.environ['db_uri'])
    app.include_router(core_router)
    return app


app = create_app()


@app.exception_handler(Exception)
async def unexpected_error_log(request, ex):
    logger.error(ex)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=None,
    )
