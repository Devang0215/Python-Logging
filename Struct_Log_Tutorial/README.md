# my_logger 

## A lightweight  Structed logging Library for the Structured logging and tracing using structlog and Open Telemetry.

# Features Provided
- Structured Logging 
- Http request Response Logging middle ware for Fast API Applications 
- Automatic Trace ID and span ID injectionn using log Using OpenTelemetry
- Strutures JSON 
- OpenTelemetry supports the Metrics,loga and traces


### Structure of the library

```
mylogger/
│
├── mylogger/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── processors.py
│   ├── formatters.py
│   ├── context.py
│   ├── middleware.py
│   └── exceptions.py
│
├── examples/
│   ├── basic.py
│   ├── fastapi_example.py
│   └── django_example.py
│
├── tests/
│
├── pyproject.toml
├── README.md
└── LICENSE
```

# For Installing 

uv pip install "git+ssh://git@github.com/Devang0215/Python-Logging.git#subdirectory=Struct_Log_Tutorial"
