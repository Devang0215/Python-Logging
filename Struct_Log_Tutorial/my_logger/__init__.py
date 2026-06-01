from .config import configure_logger

from .logger import get_logger

from .telemetry import setup_tracing

from .middleware import logging_middleware

from .metrics import router as metrics_router


def setup_metrics(app):
    app.include_router(metrics_router)
