from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel, PrimaryKey

if TYPE_CHECKING:
    from .seat_booking import SeatBookingModel
    from .show import ShowModel
    from .user import UserModel


# fmt: off
class BookingModel(BaseModel):
    __tablename__ = "booking"

    booking_id:  Mapped[PrimaryKey]
    status:      Mapped[str]
    seat_count:  Mapped[int]
    total_price: Mapped[int]
    booked_at:   Mapped[datetime]

    show_id: Mapped[int]         = mapped_column(ForeignKey("show.show_id"))
    show:    Mapped["ShowModel"] = relationship("ShowModel", back_populates="bookings")

    user_id: Mapped[int]         = mapped_column(ForeignKey("user.user_id"))
    user:    Mapped["UserModel"] = relationship("UserModel", back_populates="bookings")

    seat_bookings: Mapped[list["SeatBookingModel"]] = relationship("SeatBookingModel", back_populates="booking")  # noqa: E501


class Booking(Base):
    booking_id:  int
    status:      str
    seat_count:  int
    total_price: int
    booked_at:   datetime


class BookingUpsert(Base):
    status:      str
    seat_count:  int
    total_price: int
    booked_at:   datetime
    show_id:     int
    user_id:     int
