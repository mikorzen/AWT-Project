from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base, BaseModel, PrimaryKey

if TYPE_CHECKING:
    from .seat import SeatModel


# fmt: off
class SeatTypeModel(BaseModel):
    __tablename__ = "seat_type"

    seat_type_id: Mapped[PrimaryKey]
    type:         Mapped[str]
    price:        Mapped[int]

    seats: Mapped[list["SeatModel"]] = relationship("SeatModel", back_populates="seat_type")  # noqa: E501


class SeatType(Base):
    seat_type_id: int
    type:         str
    price:        int


class SeatTypeUpsert(Base):
    type:  str
    price: int
