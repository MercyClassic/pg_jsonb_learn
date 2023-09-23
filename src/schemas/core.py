from typing import List, Dict, Annotated

from fastapi import Query
from pydantic import BaseModel, field_validator


class PrepareInfoValidator:
    @field_validator('info')
    def prepare_info_columns(cls, value):
        value['columns'] = list(
            map(
                lambda v: v.strip("'"),
                value.get('columns').strip('[]').split(', '),
            ),
        )
        return value


class CSVFileSchemaList(BaseModel, PrepareInfoValidator):
    id: int
    info: dict

    class Config:
        from_attributes = True


class CSVFileSchemaDetail(BaseModel, PrepareInfoValidator):
    id: int
    info: dict
    rows: List[Dict]

    class Config:
        from_attributes = True


class FilterCSVFile(BaseModel):
    sort_by: Annotated[str | None, Query(default=None)]
    ascending: Annotated[bool | None, Query(default=True)]

    @field_validator('sort_by')
    def prepare_sort_by(cls, value):
        if value:
            return value.lower()
