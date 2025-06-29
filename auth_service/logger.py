"""Logging"""

import logging
import sys

from config import settings

LOG_LEVEL = settings.LOG_LEVEL

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"


def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
    # Override uvicorn loggers
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = True
        uvicorn_logger.setLevel(LOG_LEVEL)


def get_logger(name: str):
    """Get logger"""
    return logging.getLogger(name)


auth_logger = get_logger("auth")
