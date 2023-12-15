from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env', '../.env'), extra='ignore')

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    POSTGRES_USER_TEST: str
    POSTGRES_PASSWORD_TEST: str
    POSTGRES_HOST_TEST: str
    POSTGRES_DB_TEST: str

    ROOT_DIR: str = '%s' % Path(__file__).parent.parent
    MEDIA_CSV_PATH: str = 'media/csv'

    @property
    def db_uri(self) -> str:
        return 'postgresql+asyncpg://%s:%s@%s:5432/%s' % (
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_DB,
        )

    @property
    def test_db_uri(self) -> str:
        return 'postgresql+asyncpg://%s:%s@%s:5432/%s' % (
            self.POSTGRES_USER_TEST,
            self.POSTGRES_PASSWORD_TEST,
            self.POSTGRES_HOST_TEST,
            self.POSTGRES_DB_TEST,
        )

    @property
    def media_dir(self) -> str:
        return '%s/%s' % (self.ROOT_DIR, self.MEDIA_CSV_PATH)


def get_config() -> Config:
    return Config()
