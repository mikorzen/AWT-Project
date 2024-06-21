from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel, PrimaryKey

if TYPE_CHECKING:
    from .booking import BookingModel
    from .seat import SeatModel


# fmt: off
class SeatBookingModel(BaseModel):
    __tablename__ = "seat_booking"

    seat_booking_id: Mapped[PrimaryKey]

    seat_id: Mapped[int] = mapped_column(ForeignKey("seat.seat_id"))
    seat:    Mapped["SeatModel"] = relationship(
        "SeatModel",
        back_populates="seat_bookings",
    )

    booking_id: Mapped[int] = mapped_column(ForeignKey("booking.booking_id"))
    booking:    Mapped["BookingModel"] = relationship(
        "BookingModel",
        back_populates="seat_bookings",
    )


class SeatBooking(Base):
    seat_booking_id: int
    seat_id: int
    booking_id: int


class SeatBookingUpsert(Base):
    seat_id: int
    booking_id: int
