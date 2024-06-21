from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel, PrimaryKey

if TYPE_CHECKING:
    from .screen import ScreenModel
    from .seat_booking import SeatBookingModel
    from .seat_type import SeatTypeModel


# fmt: off
class SeatModel(BaseModel):
    __tablename__ = "seat"

    seat_id: Mapped[PrimaryKey]
    row:     Mapped[int]
    number:  Mapped[int]
    status:  Mapped[str]

    seat_type_id: Mapped[int]             = mapped_column(ForeignKey("seat_type.seat_type_id"))  # noqa: E501
    seat_type:    Mapped["SeatTypeModel"] = relationship("SeatTypeModel", back_populates="seats")  # noqa: E501

    screen_id: Mapped[int]           = mapped_column(ForeignKey("screen.screen_id"))
    screen:    Mapped["ScreenModel"] = relationship("ScreenModel", back_populates="seats") # noqa: E501

    seat_bookings: Mapped[list["SeatBookingModel"]] = relationship("SeatBookingModel", back_populates="seat")  # noqa: E501


class Seat(Base):
    seat_id: int
    row:     int
    number:  int
    status:  str


class SeatUpsert(Base):
    row:     int
    number:  int
    status:  str
    seat_type_id: int
    screen_id: int
