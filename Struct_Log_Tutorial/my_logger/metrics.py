from prometheus_client import (
    Counter,
    Histogram,
    Gauge
)


REQUEST_COUNT = Counter(

    "http_requests_total",

    "Total HTTP requests",

    ["method", "endpoint", "status"]
)


REQUEST_LATENCY = Histogram(

    "http_request_duration_seconds",

    "HTTP request latency",

    ["method", "endpoint"]
)



ERROR_COUNT = Counter(

    "http_errors_total",

    "Total HTTP errors",

    ["method", "endpoint"]
)


ACTIVE_REQUESTS = Gauge(

    "active_requests",

    "Currently active requests"
)