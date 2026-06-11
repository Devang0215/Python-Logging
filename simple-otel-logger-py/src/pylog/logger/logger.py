import structlog
import logging
from opentelemetry import trace


def add_open_telemetry_spans(_, __, event_dict):
    span = trace.get_current_span()
    if not span.is_recording():
        event_dict["span"] = None
        return event_dict

    ctx = span.get_span_context()
    parent = getattr(span, "parent", None)

    event_dict["span"] = {
        "span_id": format(ctx.span_id, "016x"),
        "trace_id": format(ctx.trace_id, "032x"),
        "parent_span_id": None if not parent else format(parent.span_id, "016x"),
    }

    return event_dict
def log_configure():
    # Initialises the struture of the code 
    structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                add_open_telemetry_spans,
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S',utc=False),
                structlog.processors.JSONRenderer(indent=4)
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=False
        )

class Logger():
    def __init__(self,service_name):
        log_configure()
        self.logger = structlog.get_logger().bind(service_name = service_name)
    
    def info(self,message,**kwargs):
        self.logger.info(message,**kwargs)

    def error(self,message,**kwargs):
        self.logger.error(message,**kwargs)
    
    def warning(self,message,**kwargs):
        self.logger.warning(message,**kwargs)

    def debug(self,message,**kwargs):
        self.logger.debug(message,**kwargs) 

    
  

logger = Logger("App-service")
logger.info("Hello Everyone")

