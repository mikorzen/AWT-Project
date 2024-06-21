import os

import models
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

load_dotenv()

# fmt: off
DB_MS  = "postgresql"
DB_API = "asyncpg"
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
# fmt: on

DB_URL = f"{DB_MS}+{DB_API}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Database:
    def __init__(self: "Database") -> None:
        self._engine = create_async_engine(DB_URL, echo=True)

    @property
    def engine(self: "Database") -> AsyncEngine:
        return self._engine

    async def create_tables(self: "Database") -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(models.BaseModel.metadata.create_all)

    async def drop_tables(self: "Database") -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(models.BaseModel.metadata.drop_all)


database = Database()
