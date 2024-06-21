from typing import Annotated

from pydantic import BaseModel as _BaseModel
from sqlalchemy.orm import DeclarativeBase, mapped_column

PrimaryKey = Annotated[int, mapped_column(primary_key=True)]


class Base(_BaseModel):
    # Validation (Pydantic) model
    model_config = {"from_attributes": True}


class BaseModel(DeclarativeBase):
    # ORM (SQLAlchemy) model
    pass
