import logging
from app.core.config import settings

logging.basicConfig(
    level=logging.DEBUG
    if settings.debug
    else logging.INFO,  # Cambia a DEBUG si estás desarrollando
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logger = logging.getLogger("app")
