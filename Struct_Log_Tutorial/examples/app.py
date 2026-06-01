import time
import uuid


from prometheus_client import generate_latest

from fastapi import FastAPI, Response
from my_logger.logger import AppLogger


from my_logger import configure_logger, get_logger

from my_logger.telemetry import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

setup_tracing()

configure_logger(json_logs=True)

log = get_logger("fastapi-app")

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)


@app.get("/")
async def home():
    log.info("home_route_called")

    return {"message": "Hello"}


@app.get("/upload")
async def upload():

    log.info("upload_route_called")

    return {"message": "Upload"}


@app.get("/users")
async def users():

    log.info("fetching_users")

    return {"users": []}


@app.get("/payment")
async def payment():

    log = AppLogger("payment-service")

    log.info("payment_success", time=int(time.time()), transaction_id=str(uuid.uuid4()))

    return {"users": []}


@app.get("/metrics")
async def metrics():

    return Response(generate_latest(), media_type="text/plain")


# #  For Middlewares


# # @app.middleware("http")
# # async def logging_middleware(
# #     request: Request,
# #     call_next
# # ):

# #     start_time = time.time()

# #     request_id = str(uuid.uuid4())

# #     structlog.contextvars.bind_contextvars(
# #         request_id=request_id
# #     )

# #     try:

# #         log.info(
# #             "request_started",
# #             path=request.url.path,
# #             method=request.method
# #         )

# #         response = await call_next(request)

# #         process_time = time.time() - start_time

# #         log.info(
# #             "request_completed",
# #             status_code=response.status_code,
# #             process_time=round(process_time, 4)
# #         )

# #         return response

# #     except Exception:

# #         log.exception(
# #             "request_failed"
# #         )

# #         raise

# #     finally:

# #         structlog.contextvars.clear_contextvars()

# @app.middleware("http")
# async def metrics_middleware(
#     request: Request,
#     call_next
# ):

#     ACTIVE_REQUESTS.inc()

#     start_time = time.time()

#     try:

#         response = await call_next(request)

#         duration = time.time() - start_time

#         REQUEST_COUNT.labels(

#             method=request.method,

#             endpoint=request.url.path,

#             status=response.status_code

#         ).inc()

#         REQUEST_LATENCY.labels(

#             method=request.method,

#             endpoint=request.url.path

#         ).observe(duration)

#         return response

#     except Exception:

#         ERROR_COUNT.labels(

#             method=request.method,

#             endpoint=request.url.path

#         ).inc()

#         raise

#     finally:

#         ACTIVE_REQUESTS.dec()
