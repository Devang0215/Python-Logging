from .config import configure_logger
from .logger import get_logger as get_logger
from .metrics import router as metrics_router
from .middleware import logging_middleware as logging_middleware
from .telemetry import create_span, setup_tracing


def setup_metrics(app):
    app.include_router(metrics_router)


configure_logger()
setup_tracing()
