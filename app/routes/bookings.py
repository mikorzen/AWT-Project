from typing import Annotated

from configuration import database
from litestar import Controller, delete, get, patch, post
from litestar.params import Body
from models import Booking, BookingModel, BookingUpsert
from pydantic import TypeAdapter
from sqlalchemy import delete as sql_delete
from sqlalchemy import insert, select, update

BookingBody = Annotated[BookingUpsert, Body]


class BookingsController(Controller):
    path = "/bookings"

    @get()
    async def get_bookings(self: "BookingsController") -> list[Booking]:
        async with database.engine.connect() as connection:
            statement = select(BookingModel)
            result = await connection.execute(statement)
            bookings = result.all()

        type_adapter = TypeAdapter(list[Booking])
        return type_adapter.validate_python(bookings)

    @get("{booking_id:int}")
    async def get_booking(self: "BookingsController", booking_id: int) -> Booking:
        async with database.engine.connect() as connection:
            statement = select(BookingModel).where(
                BookingModel.booking_id == booking_id,
            )
            result = await connection.execute(statement)
            booking = result.mappings().first()
        return Booking.model_validate(booking)

    @post()
    async def create_booking(
        self: "BookingsController",
        data: BookingBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = insert(BookingModel).values(
                status=data.status,
                seat_count=data.seat_count,
                total_price=data.total_price,
                booked_at=data.booked_at,
                show_id=data.show_id,
                user_id=data.user_id,
            )
            await connection.execute(statement)
            await connection.commit()

    @patch("{booking_id:int}")
    async def update_booking(
        self: "BookingsController",
        booking_id: int,
        data: BookingBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = (
                update(BookingModel)
                .where(BookingModel.booking_id == booking_id)
                .values(
                    status=data.status,
                    seat_count=data.seat_count,
                    total_price=data.total_price,
                    booked_at=data.booked_at,
                    show_id=data.show_id,
                    user_id=data.user_id,
                )
            )
            await connection.execute(statement)
            await connection.commit()

    @delete("{booking_id:int}")
    async def delete_booking(self: "BookingsController", booking_id: int) -> None:
        async with database.engine.connect() as connection:
            statement = sql_delete(BookingModel).where(
                BookingModel.booking_id == booking_id,
            )
            await connection.execute(statement)
            await connection.commit()
