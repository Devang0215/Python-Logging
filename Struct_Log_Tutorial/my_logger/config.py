import logging
import structlog
from .processors import *

from .settings import (
    LOG_LEVEL,
    JSON_LOGS
)
console_handler = logging.StreamHandler()

file_handler = logging.FileHandler(
    "app.log"
)


def configure_logger(json_logs=False,log_level="INFO"):

    renderer = (structlog.processors.JSONRenderer(indent=4,sort_keys=True) if json_logs else structlog.dev.ConsoleRenderer())

    logging.basicConfig(
        handlers=[console_handler, file_handler],
        format="%(message)s",
        level=log_level
    )

    structlog.configure(
        processors = [
            structlog.contextvars.merge_contextvars,
            add_app_metadata,
            add_trace_context,
            mask_sensitive_data,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),

            renderer
        ],

        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True
    )

