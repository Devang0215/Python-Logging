import structlog

from .settings import SERVICE_NAME


def get_logger():
    print(SERVICE_NAME)
    return structlog.get_logger().bind(service=SERVICE_NAME)
