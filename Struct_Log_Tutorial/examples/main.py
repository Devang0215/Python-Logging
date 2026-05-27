# from my_logger.logger import setup_logger
# from rich.console import Console

# console = Console()


# logger = setup_logger()


# logger.info(
#     "user_login",
#     user_id=123,
#     status="success",
#     action="login"
# )

# logger.info(
#     "user_login",
#     user_id=12111,
#     status="failure",
#     action="login",
#     stack_info=True
# )



import structlog

def add_app_name(logger,method_name,event_dict):
    event_dict["app_name"] = "Auth_Service"

    return event_dict

def add_environemnt(logger,method_name,event_dict):
    event_dict["environment"] = "production"

    return event_dict

def add_severity(logger, method_name, event_dict):

    event_dict["severity"] = method_name.upper()

    return event_dict


def ignore_debug(logger, method_name, event_dict):

    if method_name == "info":
        raise structlog.DropEvent

    return event_dict

structlog.configure(
    processors=[
        add_app_name,
        add_environemnt,
        add_severity,
        # ignore_debug,
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        # structlog.dev.ConsoleRenderer()
        structlog.processors.JSONRenderer(indent=4,sort_keys=True),
        # structlog.processors.KeyValueRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),

    cache_logger_on_first_use=True
)

log = structlog.get_logger().bind(service="my_service")

structlog.contextvars.bind_contextvars(
    request_id="REQ-101",
    user_id=45,
    service="payment-api"
)


log.info(
    "user_login",
    username="devang",
    status="success",
    # stack_info=True
)


log.info(
    "SessionLogin",
    username="devangkamdar",
    status="success",
    # stack_info=True
)
# try:
#     1 / 0

# except Exception:
#     log.exception("division_failed")