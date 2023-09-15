from typing import List

from fastapi import Depends, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from pydantic import TypeAdapter
from starlette import status
from starlette.responses import JSONResponse

from dependencies.core import get_core_service
from schemas.core import CSVFileSchema
from services.core import CoreService

router = APIRouter(tags=['core'], prefix='/api/v1')


@router.post('/')
async def send_file(
    file: UploadFile,
    core_service: CoreService = Depends(get_core_service),
):
    file = await core_service.save_file(file)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'file': jsonable_encoder(file)},
    )


@router.get('/')
async def get_file_list(core_service: CoreService = Depends(get_core_service)):
    files = await core_service.get_files()
    data = TypeAdapter(List[CSVFileSchema]).validate_python(files)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'file': jsonable_encoder(data)})


@router.get('/{file_id}')
async def get_file_detail(
    file_id: int,
    core_service: CoreService = Depends(get_core_service),
):
    file = await core_service.get_file(file_id)
    data = TypeAdapter(CSVFileSchema).validate_python(file)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'file': jsonable_encoder(data)})
