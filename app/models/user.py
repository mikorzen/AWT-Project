import uuid
from typing import TYPE_CHECKING

import sqlalchemy.dialects.postgresql as psql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel, PrimaryKey

if TYPE_CHECKING:
    from .booking import BookingModel


# fmt: off
class UserModel(BaseModel):
    __tablename__ = "user"

    user_id:    Mapped[PrimaryKey]
    user_uuid:  Mapped[uuid.UUID] = mapped_column(psql.UUID(as_uuid=True), default=uuid.uuid4())  # noqa: E501
    last_name:  Mapped[str]
    first_name: Mapped[str]
    username:   Mapped[str]
    password:   Mapped[str]
    created_at: Mapped[psql.TIMESTAMP] = mapped_column(psql.TIMESTAMP, server_default="now()")  # noqa: E501

    bookings: Mapped[list["BookingModel"]] = relationship("BookingModel", back_populates="user")  # noqa: E501


class User(Base):
    user_uuid:  uuid.UUID
    last_name:  str
    first_name: str
    username:   str
    password:   str
    created_at: int


class UserUpsert(Base):
    last_name:  str
    first_name: str
    username:   str
    password:   str
    created_at: int
