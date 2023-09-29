from typing import List, Type

from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.core import CSVFile


class CoreRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, json_data: dict) -> Type[CSVFile]:
        stmt = insert(CSVFile).values(info=json_data).returning(CSVFile)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def get_all(self) -> List[Type[CSVFile]]:
        query = select(CSVFile)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, file_id: int) -> Type[CSVFile]:
        query = select(CSVFile).where(CSVFile.id == file_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def is_has_column(self, file_id: int, column: str) -> bool:
        query = select(1).where(
            and_(
                CSVFile.id == file_id,
                CSVFile.info['columns'].astext.like(f'%{column}%'),
            ),
        )
        result = await self.session.execute(query)
        return bool(result.scalar())
