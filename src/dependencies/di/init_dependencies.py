from functools import partial

from fastapi import FastAPI

from config import Config, WebConfig, WebConfigProvider
from db.database import create_async_session_maker, get_async_session, get_session_stub


def init_dependencies(app: FastAPI, db_uri: str) -> None:
    async_session_maker = create_async_session_maker(db_uri)

    config = Config()
    web_config_provider = WebConfigProvider(config.media_dir)

    app.dependency_overrides[WebConfig] = web_config_provider
    app.dependency_overrides[get_session_stub] = partial(
        get_async_session,
        async_session_maker,
    )
