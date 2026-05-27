import structlog

from .settings import (
    SERVICE_NAME
)


def get_logger():

    return structlog.get_logger().bind(
        service=SERVICE_NAME
    )