from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

<<<<<<< HEAD
=======
from opentelemetry.sdk.trace import TracerProvider

>>>>>>> 926814889587ec2268b0c6dbb1f54e8cc6f6e15b

def setup_tracing():

    trace.set_tracer_provider(TracerProvider())
