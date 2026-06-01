from fastapi import FastAPI

from fastapi.responses import Response

from prometheus_client import generate_latest

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from mylogger import configure_logger, get_logger, setup_tracing, logging_middleware

setup_tracing()

configure_logger()

log = get_logger()

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)

app.middleware("http")(logging_middleware)


@app.get("/")
async def home():

    log.info("home_called")

    return {"message": "hello"}


@app.get("/error")
async def error():

    1 / 0


@app.get("/metrics")
async def metrics():

    return Response(generate_latest(), media_type="text/plain")
