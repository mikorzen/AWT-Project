from typing import Annotated

from configuration import database
from litestar import Controller, delete, get, patch, post
from litestar.params import Body
from models import SeatType, SeatTypeModel, SeatTypeUpsert
from pydantic import TypeAdapter
from sqlalchemy import delete as sql_delete
from sqlalchemy import insert, select, update

SeatTypeBody = Annotated[SeatTypeUpsert, Body]


class SeatTypesController(Controller):
    path = "/seat_types"

    @get()
    async def get_seat_types(self: "SeatTypesController") -> list[SeatType]:
        async with database.engine.connect() as connection:
            statement = select(SeatTypeModel)
            result = await connection.execute(statement)
            seat_types = result.all()

        type_adapter = TypeAdapter(list[SeatType])
        return type_adapter.validate_python(seat_types)

    @get("{seat_type_id:int}")
    async def get_seat_type(self: "SeatTypesController", seat_type_id: int) -> SeatType:
        async with database.engine.connect() as connection:
            statement = select(SeatTypeModel).where(
                SeatTypeModel.seat_type_id == seat_type_id,
            )
            result = await connection.execute(statement)
            seat_type = result.mappings().first()
        return SeatType.model_validate(seat_type)

    @post()
    async def create_seat_type(
        self: "SeatTypesController",
        data: SeatTypeBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = insert(SeatTypeModel).values(
                type=data.type,
                price=data.price,
            )
            await connection.execute(statement)
            await connection.commit()

    @patch("{seat_type_id:int}")
    async def update_seat_type(
        self: "SeatTypesController",
        seat_type_id: int,
        data: SeatTypeBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = (
                update(SeatTypeModel)
                .where(SeatTypeModel.seat_type_id == seat_type_id)
                .values(
                    type=data.type,
                    price=data.price,
                )
            )
            await connection.execute(statement)
            await connection.commit()

    @delete("{seat_type_id:int}")
    async def delete_seat_type(self: "SeatTypesController", seat_type_id: int) -> None:
        async with database.engine.connect() as connection:
            statement = sql_delete(SeatTypeModel).where(
                SeatTypeModel.seat_type_id == seat_type_id,
            )
            await connection.execute(statement)
            await connection.commit()
