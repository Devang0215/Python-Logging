import uuid
import structlog
from src.pylog.logger.logger import log_configure
import time


def add_request_id():
    request_id = uuid.uuid4()

    structlog.contextvars.bind_contextvars(request_id=request_id)

    return request_id


log_configure()


def create_log_middleware(logger, request_data, response_data):
    async def log_middleware(request, call_next):
        start_time = time.time()
        req_data = request_data(request)
        add_request_id()

        logger.info("Request Started", attributes=req_data)

        response = await call_next(request)

        duration = time.time() - start_time
        res_data = response_data(request, response)
        logger.info("Response Received", attributes=res_data, duration=duration)

        return response

    return log_middleware
