import structlog
def get_logger(service_name="app"):

    logger = structlog.get_logger().bind(service=service_name)

    return logger


class AppLogger:

    def __init__(self, service):

        self.logger = (
            structlog.get_logger()
            .bind(service=service)
        )

    def info(self, event, **kwargs):

        self.logger.info(event, **kwargs)

    def error(self, event, **kwargs):

        self.logger.error(event, **kwargs)

    def exception(self, event, **kwargs):

        self.logger.exception(event, **kwargs)