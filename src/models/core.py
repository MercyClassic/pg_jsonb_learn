from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class CSVFile(Base):
    __tablename__ = 'csv_file'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    info: Mapped[JSONB] = mapped_column(JSONB, nullable=False)
