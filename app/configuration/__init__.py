from pathlib import Path

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from .auth import authorization_url, flow, state
from .database import DB_URL as DATABASE_URL
from .database import database

# fmt: off
__all__ = [
    "DATABASE_URL", "database",
    "flow", "authorization_url", "state",
    "static_router",
    "template_config",
]
# fmt: on

STATIC_DIR = Path(__file__).resolve().parents[2] / "static"
TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"


static_router = create_static_files_router("/static", [STATIC_DIR])
template_config = TemplateConfig(
    engine=JinjaTemplateEngine,
    directory=TEMPLATE_DIR,
)
