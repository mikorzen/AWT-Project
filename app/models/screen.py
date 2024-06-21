from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base, BaseModel, PrimaryKey

if TYPE_CHECKING:
    from .seat import SeatModel
    from .show import ShowModel


# fmt: off
class ScreenModel(BaseModel):
    __tablename__ = "screen"

    screen_id:  Mapped[PrimaryKey]
    name:       Mapped[str | None]
    seat_count: Mapped[int]

    shows: Mapped[list["ShowModel"]] = relationship("ShowModel", back_populates="screen")  # noqa: E501
    seats: Mapped[list["SeatModel"]] = relationship("SeatModel", back_populates="screen")  # noqa: E501


class Screen(Base):
    screen_id:  int
    name:       str | None
    seat_count: int


class ScreenUpsert(Base):
    name:       str | None
    seat_count: int
