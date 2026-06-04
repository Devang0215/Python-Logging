from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from Pylog import (
    LoggingMiddleware,
    get_logger,
    init_telemetry,
)
from opentelemetry import trace


init_telemetry(
    service_name="app-service",
    exporter_endpoint="http://localhost:4318/v1/traces",
)

logger = get_logger("user-service")
app = FastAPI()

app.add_middleware(
    LoggingMiddleware,
    logger=logger,
)
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def home():
    span = trace.get_current_span()
    ctx = span.get_span_context()

    print("SPAN:", span)
    print("TRACE ID:", ctx.trace_id)
    print("SPAN ID:", ctx.span_id)
    print("VALID:", ctx.is_valid)

    return {"ok": True}