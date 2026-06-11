import structlog
import logging

def log_configure():
    # Initialises the struture of the code 
    structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S',utc=False),
                structlog.processors.JSONRenderer(indent=4)
            ]
        )

class Logger(logging):
    def __init__(self,service_name):
        log_configure()
        self.service_name = None

    def get_logger(self):
        return structlog.get_logger().bind(service_name = self.service_name)




logger = Logger("App-service").get_logger()

logger.info("Hello Everyone")

