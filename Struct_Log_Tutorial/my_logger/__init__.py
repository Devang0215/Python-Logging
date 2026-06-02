from .config import configure_logger
<<<<<<< HEAD
from .logger import get_logger as get_logger
=======

from .logger import get_logger as get_logger

from .telemetry import setup_tracing

>>>>>>> 926814889587ec2268b0c6dbb1f54e8cc6f6e15b
from .metrics import router as metrics_router
from .telemetry import setup_tracing



def setup_metrics(app):
    app.include_router(metrics_router)


<<<<<<< HEAD
setup_tracing()
configure_logger()
=======
configure_logger()

setup_tracing()
>>>>>>> 926814889587ec2268b0c6dbb1f54e8cc6f6e15b
