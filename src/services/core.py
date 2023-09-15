import uuid
from typing import List, Type

import pandas as pd
from fastapi import UploadFile

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
        filename = uuid.uuid4()
        with open(f'media/csv/{filename}.csv', 'wb') as f:
            f.write(await file.read())
        df = pd.read_csv(f'media/csv/{filename}.csv')

        data = {'filename': filename, 'size': file.size, 'columns': df.columns._data}

        json_data = self.to_json(data)
        file = await self.repo.save(json_data)
        return file

    async def get_files(self) -> List[Type[CSVFile]]:
        files = await self.repo.get_all()
        return files

    async def get_file(self, file_id: int) -> Type[CSVFile]:
        file = await self.repo.get_by_id(file_id)
        return file
