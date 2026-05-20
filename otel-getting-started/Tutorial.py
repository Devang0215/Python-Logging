import logging
import structlog

# log = structlog.get_logger(__name__)

# log.info(
#     "user_login",
#     user_id=123,
#     username="devang",
#     status="success"
# )
# log.warning("This is a warning message")
# log.error("This is an error message")


logging.basicConfig(
    filename="app.log",
    format="%(message)s",
    level=logging.INFO,
)


structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

log = structlog.get_logger()

log.info(
    "Server Started",
    user_id=123,
    country="India",
    port=8000
    )
