from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from importlib.metadata import packages_distributions


resource = Resource.create(attributes={SERVICE_NAME: packages_distributions()["pylog"][0]})

tracerProvider = TracerProvider(resource=resource)

trace.set_tracer_provider(TracerProvider())


def get_tracer():
    provider = trace.get_tracer_provider()
    if not isinstance(provider, TracerProvider):
        trace.set_tracer_provider(TracerProvider())
    return trace.get_tracer(__name__)


def add_traces_span_exporter(OTLP_Span_exporter_endpoint=None):
    if OTLP_Span_exporter_endpoint:
        processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_Span_exporter_endpoint))
        tracerProvider.add_span_processor(processor)
        trace.set_tracer_provider(tracerProvider)


def add_metric_exporter(OTLP_Metric_exporter_endpoint=None):
    if OTLP_Metric_exporter_endpoint:
        reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=OTLP_Metric_exporter_endpoint))
        meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
        metrics.set_meter_provider(meterProvider)
