from configuration import authorization_url, database, static_router, template_config
from litestar import Litestar, get
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.response import Redirect, Template
from routes import (
    BookingsController,
    MoviesController,
    ScreensController,
    SeatBookingsController,
    SeatsController,
    SeatTypesController,
    ShowsController,
    UsersController,
)


@get("/")
async def index() -> Template:
    return HTMXTemplate(template_name="index.html")


@get("/flush")
async def flush() -> Template:
    await database.drop_tables()
    await database.create_tables()
    return HTMXTemplate(template_name="index.html")


@get("/login")
async def login() -> Redirect:
    return Redirect(authorization_url)


app = Litestar(
    route_handlers=[
        static_router,
        index,
        flush,
        login,
        BookingsController,
        MoviesController,
        ScreensController,
        SeatBookingsController,
        SeatTypesController,
        SeatsController,
        ShowsController,
        UsersController,
    ],
    template_config=template_config,
    openapi_config=OpenAPIConfig(
        title="Litestar Example",
        description="An example of a Litestar application",
        version="1.0.0",
        render_plugins=[SwaggerRenderPlugin()],
    ),
)
