from fastapi import HTTPException
from starlette import status


class NotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File Not Found',
        )


class UnsupportedFileType(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Unsupported file type',
        )
