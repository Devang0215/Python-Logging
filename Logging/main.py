from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# =============================================================
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.metrics import set_meter_provider,get_meter
# ==============================================================
from Pylog import (
    LoggingMiddleware,
    get_logger,
    init_telemetry,
    traced,
)

init_telemetry(
    service_name="app-service",
    # Here Jaeger Has Been Used
    trace_exporter_endpoint="http://localhost:4318/v1/traces",
    metric_exporter_endpoint="http://localhost:4318/v1/metrics",
    log_exporter_endpoint="http://localhost:4318/v1/logs",
    environment="development",
)
# ================================
provider = MeterProvider()

set_meter_provider(provider)

meter = get_meter(
    name="My application",
    version="1.0.0"
)


counter = meter.create_counter(
    name="requests_total",
    description="Total number of requests",
    unit="1",
)

histogram = meter.create_histogram(
    "request_duration_ms"
)

histogram.record(250)
histogram.record(100)
histogram.record(500)
# ============================

logger = get_logger(service_name="Post-doc-service")


app = FastAPI()

app.add_middleware(
    LoggingMiddleware,
    logger=logger,
    environment="development",
    request_data=lambda req: {
        "method": req.method,
        "path": req.url.path,
        "query_params": str(req.query_params),
        "client_ip": req.client.host if req.client else None,
        "url": str(req.url),
        "ip_address": req.client.host if req.client else None,
        "user_agent": req.headers.get("user-agent"),
    },
    response_data=lambda req, res: {
        "status_code": res.status_code,
        "url": str(req.url),
        "handler": req.scope.get("endpoint").__name__ if req.scope.get("endpoint") else None,
    },
)

FastAPIInstrumentor.instrument_app(app)


@app.get("/")
async def home():
    logger.info(
        "Home endpoint called",
        event_name="home_request",
    )
    print("This is a log message from the home endpoint")
    return {
        "ok": True,
    }


@app.get("/users/{user_id}")
@traced()
async def get_user(user_id: int):

    logger.info(
        message="Fetching user",
        event_name="get_user",
        user_id=user_id,
    )
    await new_message()
    return {
        "user_id": user_id,
    }


@traced()
async def new_message():
    logger.warn(
        message="I am inside the new_message function",
        event_name="new_message",
    )


@app.get("/error")
async def error():
    logger.error(
        "Test error generated",
        event_name="test_error",
    )

    raise Exception("Sample Exception")
