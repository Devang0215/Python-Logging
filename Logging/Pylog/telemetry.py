from opentelemetry import _logs, metrics, trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import (
    ConsoleLogExporter,
    SimpleLogRecordProcessor,
)

# Metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource

# Traces
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

_started = False


def init_telemetry(
    service_name: str,
    trace_exporter_endpoint: str,
    metric_exporter_endpoint: str | None = None,
    log_exporter_endpoint: str | None = None,
    environment: str = "development",
):
    global _started

    if _started:
        return

    resource = Resource.create(
        {
            "service.name": service_name,
            "deployment.environment": environment,
        }
    )

    tracer_provider = TracerProvider(resource=resource)

    # trace_exporter = OTLPSpanExporter(
    #     endpoint=trace_exporter_endpoint,
    # )

    # tracer_provider.add_span_processor(trace_exporter)

    if environment != "production":
        tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(tracer_provider)

    if metric_exporter_endpoint:
        metric_exporter = OTLPMetricExporter(
            endpoint=metric_exporter_endpoint,
        )

        metric_reader = PeriodicExportingMetricReader(
            exporter=metric_exporter,
            export_interval_millis=5000,
        )

        meter_provider = MeterProvider(
            resource=resource,
            metric_readers=[metric_reader],
        )

        metrics.set_meter_provider(meter_provider)

    # Optional Console Metrics
    elif environment != "production":
        metric_reader = PeriodicExportingMetricReader(
            exporter=ConsoleMetricExporter(),
            export_interval_millis=5000,
        )

        meter_provider = MeterProvider(
            resource=resource,
            metric_readers=[metric_reader],
        )

        metrics.set_meter_provider(meter_provider)

    logger_provider = LoggerProvider(
        resource=resource,
    )

    if environment != "production":
        logger_provider.add_log_record_processor(
            SimpleLogRecordProcessor(ConsoleLogExporter())
        )


    _logs.set_logger_provider(logger_provider)

    _started = True
