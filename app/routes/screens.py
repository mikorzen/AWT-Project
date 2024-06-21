from typing import Annotated

from configuration import database
from litestar import Controller, delete, get, patch, post
from litestar.params import Body
from models import Screen, ScreenModel, ScreenUpsert
from pydantic import TypeAdapter
from sqlalchemy import delete as sql_delete
from sqlalchemy import insert, select, update

ScreenBody = Annotated[ScreenUpsert, Body]


class ScreensController(Controller):
    path = "/screens"

    @get()
    async def get_screens(self: "ScreensController") -> list[Screen]:
        async with database.engine.connect() as connection:
            statement = select(ScreenModel)
            result = await connection.execute(statement)
            screens = result.all()

        type_adapter = TypeAdapter(list[Screen])
        return type_adapter.validate_python(screens)

    @get("{screen_id:int}")
    async def get_screen(self: "ScreensController", screen_id: int) -> Screen:
        async with database.engine.connect() as connection:
            statement = select(ScreenModel).where(ScreenModel.screen_id == screen_id)
            result = await connection.execute(statement)
            screen = result.mappings().first()
        return Screen.model_validate(screen)

    @post()
    async def create_screen(
        self: "ScreensController",
        data: ScreenBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = insert(ScreenModel).values(
                name=data.name,
                seat_count=data.seat_count,
            )
            await connection.execute(statement)
            await connection.commit()

    @patch("{screen_id:int}")
    async def update_screen(
        self: "ScreensController",
        screen_id: int,
        data: ScreenBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = (
                update(ScreenModel)
                .where(ScreenModel.screen_id == screen_id)
                .values(
                    name=data.name,
                    seat_count=data.seat_count,
                )
            )
            await connection.execute(statement)
            await connection.commit()

    @delete("{screen_id:int}")
    async def delete_screen(self: "ScreensController", screen_id: int) -> None:
        async with database.engine.connect() as connection:
            statement = sql_delete(ScreenModel).where(
                ScreenModel.screen_id == screen_id,
            )
            await connection.execute(statement)
            await connection.commit()
