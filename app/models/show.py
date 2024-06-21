from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel, PrimaryKey

if TYPE_CHECKING:
    from .booking import BookingModel
    from .movie import MovieModel
    from .screen import ScreenModel


# fmt: off
class ShowModel(BaseModel):
    __tablename__ = "show"

    show_id: Mapped[PrimaryKey]
    time:    Mapped[time]
    date:    Mapped[date]

    screen_id: Mapped[int]           = mapped_column(ForeignKey("screen.screen_id"))
    screen:    Mapped["ScreenModel"] = relationship("ScreenModel", back_populates="shows")  # noqa: E501

    movie_id: Mapped[int]          = mapped_column(ForeignKey("movie.movie_id"))
    movie:    Mapped["MovieModel"] = relationship("MovieModel", back_populates="shows")

    bookings: Mapped[list["BookingModel"]] = relationship("BookingModel", back_populates="show")  # noqa: E501


class Show(Base):
    show_id: int
    time:    time
    date:    date


class ShowUpsert(Base):
    time:      time
    date:      date
    movie_id:  int
    screen_id: int
