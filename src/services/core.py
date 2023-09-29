import uuid
from typing import List, Type

import pandas as pd
from fastapi import UploadFile

from config import settings
from exceptions.core import ColumnNotFound, NotFound, UnsupportedFileType
from models.core import CSVFile
from repositories.core import CoreRepository


class CoreService:
    def __init__(self, repo: CoreRepository):
        self.repo = repo

    @staticmethod
    def check_content_type(content_type: str) -> bool:
        return content_type == 'text/csv'

    @staticmethod
    def to_json(data: dict):
        return dict(map(lambda value: (value[0], str(value[1])), data.items()))

    async def save_file(self, file: UploadFile) -> Type[CSVFile]:
        if not self.check_content_type(file.content_type):
            raise UnsupportedFileType

        filename = uuid.uuid4()
        with open(f'{settings.MEDIA_CSV_PATH}{filename}.csv', 'wb') as f:
            f.write(await file.read())
        df = pd.read_csv(f'{settings.MEDIA_CSV_PATH}{filename}.csv')

        data = {
            'filename': filename,
            'size': file.size,
            'columns': list(df.columns),
        }

        json_data = self.to_json(data)
        file = await self.repo.save(json_data)
        return file

    async def get_files(self) -> List[Type[CSVFile]]:
        files = await self.repo.get_all()
        return files

    async def get_file(self, file_id: int) -> Type[CSVFile]:
        file = await self.repo.get_by_id(file_id)
        if not file:
            raise NotFound
        return file

    async def get_file_data(
        self,
        filename: str,
        filters: dict,
    ):
        df = pd.read_csv(f'{settings.MEDIA_CSV_PATH}{filename}.csv')

        sort_by = filters.get('sort_by')
        if sort_by:
            try:
                df = df.sort_values(sort_by, ascending=filters['ascending'])
            except KeyError:
                raise ColumnNotFound

        data = [(dict(zip(df.columns.values, row))) for row in df.values]
        return data

    async def is_column_exists(
        self,
        file_id: int,
        column: str,
    ) -> bool:
        data = await self.repo.is_has_column(file_id, column)
        return data
