import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        logger,
        environment="development",
    ):
        super().__init__(app)

        self.logger = logger
        self.environment = environment

    async def dispatch(
        self,
        request,
        call_next,
    ):

        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())

        start_time = time.time()

        self.logger.info(
            "HTTP request received",
            event_name="http_request_start",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            environment=self.environment,
        )

        response = await call_next(request)

        duration = round(
            time.time() - start_time,
            4,
        )

        if response.status_code >= 500:
            self.logger.error(
                "HTTP error response",
                event_name="http_error",
                request_id=request_id,
                status_code=response.status_code,
            )

        self.logger.info(
            "HTTP response sent",
            event_name="http_request_complete",
            request_id=request_id,
            status_code=response.status_code,
            duration=duration,
        )

        return response
