from typing import Annotated

from configuration import database
from litestar import Controller, delete, get, patch, post
from litestar.params import Body
from models import Show, ShowModel, ShowUpsert
from pydantic import TypeAdapter
from sqlalchemy import delete as sql_delete
from sqlalchemy import insert, select, update

ShowBody = Annotated[ShowUpsert, Body]


class ShowsController(Controller):
    path = "/shows"

    @get()
    async def get_shows(self: "ShowsController") -> list[Show]:
        async with database.engine.connect() as connection:
            statement = select(ShowModel)
            result = await connection.execute(statement)
            shows = result.all()

        type_adapter = TypeAdapter(list[Show])
        return type_adapter.validate_python(shows)

    @get("{show_id:int}")
    async def get_show(self: "ShowsController", show_id: int) -> Show:
        async with database.engine.connect() as connection:
            statement = select(ShowModel).where(ShowModel.show_id == show_id)
            result = await connection.execute(statement)
            show = result.mappings().first()
        return Show.model_validate(show)

    @post()
    async def create_show(
        self: "ShowsController",
        data: ShowBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = insert(ShowModel).values(
                time=data.time,
                date=data.date,
                screen_id=data.screen_id,
                movie_id=data.movie_id,
            )
            await connection.execute(statement)
            await connection.commit()

    @patch("{show_id:int}")
    async def update_show(
        self: "ShowsController",
        show_id: int,
        data: ShowBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = (
                update(ShowModel)
                .where(ShowModel.show_id == show_id)
                .values(
                    time=data.time,
                    date=data.date,
                    screen_id=data.screen_id,
                    movie_id=data.movie_id,
                )
            )
            await connection.execute(statement)
            await connection.commit()

    @delete("{show_id:int}")
    async def delete_show(self: "ShowsController", show_id: int) -> None:
        async with database.engine.connect() as connection:
            statement = sql_delete(ShowModel).where(ShowModel.show_id == show_id)
            await connection.execute(statement)
            await connection.commit()
