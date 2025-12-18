import logging
import sys

import colorlog

from app.config import DEBUG

LOG_LEVEL_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(levelname)-8s%(reset)s "
        "(%(cyan)s%(name)s%(reset)s) %(message)s",
    log_colors=LOG_LEVEL_COLORS,
)

def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)

    root_logger.debug(f"Logging initialized with DEBUG level")
