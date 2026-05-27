import logging
import os

from logging.handlers import (
    RotatingFileHandler
)

import structlog

from .settings import (
    JSON_LOGS,
    LOG_LEVEL
)

from .processors import (

    add_trace_context,

    add_app_metadata,

    mask_sensitive_data
)


def configure_logger():

    os.makedirs(
        "logs",
        exist_ok=True
    )

    file_handler = RotatingFileHandler(

        "logs/app.log",

        maxBytes=10_000_000,

        backupCount=5
    )

    logging.basicConfig(

        handlers=[
            logging.StreamHandler(),
            file_handler
        ],

        format="%(message)s",

        level=LOG_LEVEL
    )

    renderer = (

        structlog.processors.JSONRenderer()

        if JSON_LOGS

        else structlog.dev.ConsoleRenderer()
    )

    structlog.configure(

        processors=[

            structlog.contextvars.merge_contextvars,

            mask_sensitive_data,

            add_trace_context,

            add_app_metadata,

            structlog.processors.TimeStamper(
                fmt="iso"
            ),

            structlog.processors.add_log_level,

            structlog.processors.StackInfoRenderer(),

            structlog.processors.format_exc_info,

            structlog.processors.UnicodeDecoder(),

            renderer
        ],

        logger_factory=structlog.PrintLoggerFactory(),

        cache_logger_on_first_use=True
    )