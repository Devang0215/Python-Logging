from datetime import datetime

import structlog
from opentelemetry import trace


def get_otel_context():
    span = trace.get_current_span()

    if not span:
        return {}

    ctx = span.get_span_context()

    return {
        "trace_id": format(ctx.trace_id, "032x"),
        "span_id": format(ctx.span_id, "016x"),
        "trace_flags": format(ctx.trace_flags, "02x"),
    }


class Logger:
    def __init__(self, service_name="app-service"):
        self.service_name = service_name

        self.logger = structlog.get_logger()

    def _build_record(
        self,
        level,
        message,
        **kwargs,
    ):
        return {
            "severityText": level,
            "severityNumber": 1, 
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            **get_otel_context(),
            **kwargs,
        }
    def info(self, message, **kwargs):
        self.logger.info(
            message,
            **self._build_record(
                "INFO",
                message,
                **kwargs,
            ),
        )
    def error(self, message, **kwargs):
        self.logger.error(
            message,
            **self._build_record(
                "ERROR",
                message,
                **kwargs,
            ),
        )
    def warn(self, message, **kwargs):
        self.logger.warning(
            message,
            **self._build_record(
                "WARN",
                message,
                **kwargs,
            ),
        )
    def debug(self, message, **kwargs):
        self.logger.debug(
            message,
            **self._build_record(
                "DEBUG",
                message,
                **kwargs,
            ),
        )

def configure_structlog():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(indent=4),
        ]
    )

def get_logger(
    service_name="app-service",
):
    configure_structlog()
    return Logger(service_name)
