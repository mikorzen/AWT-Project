from typing import Annotated

from configuration import database
from litestar import Controller, delete, get, patch, post
from litestar.params import Body
from models import Seat, SeatModel, SeatUpsert
from pydantic import TypeAdapter
from sqlalchemy import delete as sql_delete
from sqlalchemy import insert, select, update

SeatBody = Annotated[SeatUpsert, Body]


class SeatsController(Controller):
    path = "/seats"

    @get()
    async def get_seats(self: "SeatsController") -> list[Seat]:
        async with database.engine.connect() as connection:
            statement = select(SeatModel)
            result = await connection.execute(statement)
            seats = result.all()

        type_adapter = TypeAdapter(list[Seat])
        return type_adapter.validate_python(seats)

    @get("{seat_id:int}")
    async def get_seat(self: "SeatsController", seat_id: int) -> Seat:
        async with database.engine.connect() as connection:
            statement = select(SeatModel).where(SeatModel.seat_id == seat_id)
            result = await connection.execute(statement)
            seat = result.mappings().first()
        return Seat.model_validate(seat)

    @post()
    async def create_seat(
        self: "SeatsController",
        data: SeatBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = insert(SeatModel).values(
                row=data.row,
                number=data.number,
                status=data.status,
                seat_type_id=data.seat_type_id,
                screen_id=data.screen_id,
            )
            await connection.execute(statement)
            await connection.commit()

    @patch("{seat_id:int}")
    async def update_seat(
        self: "SeatsController",
        seat_id: int,
        data: SeatBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = (
                update(SeatModel)
                .where(SeatModel.seat_id == seat_id)
                .values(
                    row=data.row,
                    number=data.number,
                    status=data.status,
                    seat_type_id=data.seat_type_id,
                    screen_id=data.screen_id,
                )
            )
            await connection.execute(statement)
            await connection.commit()

    @delete("{seat_id:int}")
    async def delete_seat(self: "SeatsController", seat_id: int) -> None:
        async with database.engine.connect() as connection:
            statement = sql_delete(SeatModel).where(SeatModel.seat_id == seat_id)
            await connection.execute(statement)
            await connection.commit()
