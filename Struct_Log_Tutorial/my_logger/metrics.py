from prometheus_client import (
    Counter,
    Histogram,
    Gauge
)

REQUEST_COUNT = Counter(

    "http_requests_total",

    "Total HTTP Requests",

    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(

    "http_request_duration_seconds",

    "Request Latency",

    ["method", "endpoint"]
)

ERROR_COUNT = Counter(

    "http_errors_total",

    "Total Errors",

    ["method", "endpoint"]
)

ACTIVE_REQUESTS = Gauge(

    "active_requests",

    "Active Requests"
)