from pydantic import BaseModel


class CSVFileSchema(BaseModel):
    id: int
    info: dict

    class Config:
        from_attributes = True
