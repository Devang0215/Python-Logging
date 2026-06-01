import os
import logging

from logging.handlers import RotatingFileHandler

import structlog

from .settings import JSON_LOGS, LOG_LEVEL

from .processors import add_trace_context, add_app_metadata, mask_sensitive_data


def configure_logger():

    os.makedirs("logs", exist_ok=True)

    # -------------------------
    # FILE HANDLER
    # -------------------------

    file_handler = RotatingFileHandler(
        filename="logs/app.log", maxBytes=10_000_000, backupCount=5
    )

    # -------------------------
    # CONSOLE HANDLER
    # -------------------------

    console_handler = logging.StreamHandler()

    # -------------------------
    # BASIC CONFIG
    # -------------------------

    logging.basicConfig(
        handlers=[console_handler, file_handler], level=LOG_LEVEL, format="%(message)s"
    )

    # -------------------------
    # DISABLE EXTRA LOGS
    # -------------------------

    logging.getLogger("uvicorn.access").disabled = True

    logging.getLogger("opentelemetry").setLevel(logging.WARNING)

    # -------------------------
    # RENDERER
    # -------------------------

    renderer = (
        structlog.processors.JSONRenderer(indent=4)
        if JSON_LOGS
        else structlog.dev.ConsoleRenderer()
    )

    # -------------------------
    # STRUCTLOG CONFIG
    # -------------------------

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            mask_sensitive_data,
            add_trace_context,
            add_app_metadata,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            renderer,
        ],
        # IMPORTANT FIX
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
