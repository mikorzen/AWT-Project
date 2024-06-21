from typing import Annotated

from configuration import database
from litestar import Controller, get, post
from litestar.params import Body
from models import User, UserModel, UserUpsert
from pydantic import TypeAdapter
from sqlalchemy import insert, select

UserBody = Annotated[UserUpsert, Body]


class UsersController(Controller):
    path = "/users"

    @get()
    async def get_users(self: "UsersController") -> list[User]:
        async with database.engine.connect() as connection:
            statement = select(UserModel)
            result = await connection.execute(statement)
            users = result.all()

        type_adapter = TypeAdapter(list[User])
        return type_adapter.validate_python(users)

    @get("{user_id:int}")
    async def get_user(self: "UsersController", user_id: int) -> User:
        async with database.engine.connect() as connection:
            statement = select(UserModel).where(UserModel.user_id == user_id)
            result = await connection.execute(statement)
            user = result.mappings().first()
        return User.model_validate(user)

    @post()
    async def create_user(
        self: "UsersController",
        data: UserBody,
    ) -> None:
        async with database.engine.connect() as connection:
            statement = insert(UserModel).values(
                last_name=data.last_name,
                first_name=data.first_name,
                username=data.username,
                password=data.password,
            )
            await connection.execute(statement)
            await connection.commit()
