from my_logger import (
    configure_logger,
    get_logger,
    bind_request_context,
    clear_request_context
)

configure_logger(
    json_logs=True
)

log = get_logger("auth-service")

bind_request_context(
    user_id=101
)

log.info(
    "user_login",
    username="devang"
)

clear_request_context()