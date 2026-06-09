import time
import uuid

from fastapi import FastAPI, Response
from my_logger import configure_logger, get_logger
from my_logger.logger import AppLogger
from my_logger.telemetry import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import generate_latest

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
