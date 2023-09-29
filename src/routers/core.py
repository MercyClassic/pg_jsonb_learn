from typing import Annotated, List

from fastapi import Body, Depends, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from pydantic import TypeAdapter
from starlette import status
from starlette.responses import JSONResponse

from dependencies.core import get_core_service
from schemas.core import CSVFileSchemaDetail, CSVFileSchemaList, FilterCSVFile
from services.core import CoreService

router = APIRouter(tags=['core'], prefix='/api/v1')


@router.post('/')
async def send_file(
    file: UploadFile,
    core_service: CoreService = Depends(get_core_service),
):
    file = await core_service.save_file(file)
    data = TypeAdapter(CSVFileSchemaList).validate_python(file)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'file': jsonable_encoder(data)},
    )


@router.get('/')
async def get_file_list(core_service: CoreService = Depends(get_core_service)):
    files = await core_service.get_files()
    data = TypeAdapter(List[CSVFileSchemaList]).validate_python(files)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'files': jsonable_encoder(data)},
    )


@router.get('/{file_id}')
async def get_file_detail(
    file_id: int,
    filters: FilterCSVFile = Depends(),
    core_service: CoreService = Depends(get_core_service),
):
    file = await core_service.get_file(file_id)

    rows = await core_service.get_file_data(
        filename=file.info.get('filename'),
        filters=filters.model_dump(),
    )
    file.rows = rows

    data = TypeAdapter(CSVFileSchemaDetail).validate_python(file)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'file': jsonable_encoder(data)},
    )


@router.post('/{file_id}/has_column')
async def column_exists(
    file_id: int,
    column: Annotated[str, Body()],
    core_service: CoreService = Depends(get_core_service),
):
    has_column = await core_service.is_column_exists(file_id, column)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': has_column})
