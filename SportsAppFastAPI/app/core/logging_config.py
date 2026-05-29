import logging
from app.core.settings import settings


def configure_logging():
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
