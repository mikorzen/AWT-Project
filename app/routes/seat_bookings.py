from typing import Annotated

from configuration import database
from litestar import Controller, delete, get, patch, post
from litestar.params import Body
from models import SeatBooking, SeatBookingModel, SeatBookingUpsert
from pydantic import TypeAdapter
from sqlalchemy import delete as sql_delete
from sqlalchemy import insert, select, update

SeatBookingBody = Annotated[SeatBookingUpsert, Body]


class SeatBookingsController(Controller):
    path = "/seat_bookings"

    @get()
    async def get_seat_bookings(self: "SeatBookingsController") -> list[SeatBooking]:
        async with database.engine.connect() as connection:
            statement = select(SeatBookingModel)
            result = await connection.execute(statement)
            seat_bookings = result.all()

        type_adapter = TypeAdapter(list[SeatBooking])
        return type_adapter.validate_python(seat_bookings)

    @get("{seat_booking_id:int}")
    async def get_seat_booking(
        self: "SeatBookingsController",
        seat_booking_id: int,
    ) -> SeatBooking:
        async with database.engine.connect() as connection:
            statement = select(SeatBookingModel).where(
                SeatBookingModel.seat_booking_id == seat_booking_id,
            )
            result = await connection.execute(statement)
            seat_booking = result.mappings().first()
        return SeatBooking.model_validate(seat_booking)

    @post()
    async def create_seat_booking(
        self: "SeatBookingsController",
        data: SeatBookingBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = insert(SeatBookingModel).values(
                seat_id=data.seat_id,
                booking_id=data.booking_id,
            )
            await connection.execute(statement)
            await connection.commit()

    @patch("{seat_booking_id:int}")
    async def update_seat_booking(
        self: "SeatBookingsController",
        seat_booking_id: int,
        data: SeatBookingBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = (
                update(SeatBookingModel)
                .where(SeatBookingModel.seat_booking_id == seat_booking_id)
                .values(
                    seat_id=data.seat_id,
                    booking_id=data.booking_id,
                )
            )
            await connection.execute(statement)
            await connection.commit()

    @delete("{seat_booking_id:int}")
    async def delete_seat_booking(
        self: "SeatBookingsController",
        seat_booking_id: int,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = sql_delete(SeatBookingModel).where(
                SeatBookingModel.seat_booking_id == seat_booking_id,
            )
            await connection.execute(statement)
            await connection.commit()
