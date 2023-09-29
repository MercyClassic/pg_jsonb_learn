from typing import Annotated, Dict, List

from fastapi import Query
from pydantic import BaseModel, ConfigDict, field_validator


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


class CSVFileBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    info: dict


class CSVFileSchemaList(CSVFileBaseSchema, PrepareInfoValidator):
    pass


class CSVFileSchemaDetail(CSVFileBaseSchema, PrepareInfoValidator):
    rows: List[Dict]


class FilterCSVFile(BaseModel):
    sort_by: Annotated[str | None, Query(default=None)]
    ascending: Annotated[bool | None, Query(default=True)]

    @field_validator('sort_by')
    def prepare_sort_by(cls, value):
        if value:
            return value.lower()
