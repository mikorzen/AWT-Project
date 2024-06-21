from typing import Annotated

from configuration import database
from litestar import Controller, delete, get, patch, post
from litestar.params import Body
from models import Movie, MovieModel, MovieUpsert
from pydantic import TypeAdapter
from sqlalchemy import delete as sql_delete
from sqlalchemy import insert, select, update

MovieBody = Annotated[MovieUpsert, Body]


class MoviesController(Controller):
    path = "/movies"

    @get()
    async def get_movies(self: "MoviesController") -> list[Movie]:
        async with database.engine.connect() as connection:
            statement = select(MovieModel)
            result = await connection.execute(statement)
            movies = result.all()

        type_adapter = TypeAdapter(list[Movie])
        return type_adapter.validate_python(movies)

    @get("{movie_id:int}")
    async def get_movie(self: "MoviesController", movie_id: int) -> Movie:
        async with database.engine.connect() as connection:
            statement = select(MovieModel).where(MovieModel.movie_id == movie_id)
            result = await connection.execute(statement)
            movie = result.mappings().first()
        return Movie.model_validate(movie)

    @post()
    async def create_movie(
        self: "MoviesController",
        data: MovieBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = insert(MovieModel).values(
                name=data.name,
                running_time=data.running_time,
                actors=data.actors,
                languages=data.languages,
                genre=data.genre,
            )
            await connection.execute(statement)
            await connection.commit()

    @patch("{movie_id:int}")
    async def update_movie(
        self: "MoviesController",
        movie_id: int,
        data: MovieBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = (
                update(MovieModel)
                .where(MovieModel.movie_id == movie_id)
                .values(
                    name=data.name,
                    running_time=data.running_time,
                    actors=data.actors,
                    languages=data.languages,
                    genre=data.genre,
                )
            )
            await connection.execute(statement)
            await connection.commit()

    @delete("{movie_id:int}")
    async def delete_movie(self: "MoviesController", movie_id: int) -> None:
        async with database.engine.connect() as connection:
            statement = sql_delete(MovieModel).where(MovieModel.movie_id == movie_id)
            await connection.execute(statement)
            await connection.commit()
