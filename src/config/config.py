from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    ROOT_DIR: str = '%s' % Path(__file__).parent.parent
    MEDIA_CSV_PATH: str = 'media/csv'

    @property
    def media_dir(self) -> str:
        return '%s/%s' % (self.ROOT_DIR, self.MEDIA_CSV_PATH)


@dataclass
class WebConfig:
    media_dir: str


class WebConfigProvider:
    def __init__(self, media_dir: str):
        self.media_dir = media_dir

    def __call__(self) -> WebConfig:
        return WebConfig(self.media_dir)
