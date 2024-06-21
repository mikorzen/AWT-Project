from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.postgresql.array import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel, PrimaryKey

if TYPE_CHECKING:
    from .show import ShowModel


# fmt: off
class MovieModel(BaseModel):
    __tablename__ = "movie"

    movie_id:     Mapped[PrimaryKey]
    name:         Mapped[str]
    running_time: Mapped[int]
    actors:       Mapped[ARRAY] = mapped_column(ARRAY(String))
    languages:    Mapped[ARRAY] = mapped_column(ARRAY(String))
    genre:        Mapped[ARRAY] = mapped_column(ARRAY(String))

    shows: Mapped[list["ShowModel"]] = relationship("ShowModel", back_populates="movie")


class Movie(Base):
    movie_id:     int
    name:         str
    running_time: int
    actors:       list[str]
    languages:    list[str]
    genre:        list[str]


class MovieUpsert(Base):
    name:         str
    running_time: int
    actors:       list[str]
    languages:    list[str]
    genre:        list[str]
