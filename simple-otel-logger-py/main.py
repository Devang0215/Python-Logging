from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import uvicorn
from src.pylog.logger.logger import Logger, traced

from src.pylog.middleware.middleware import create_log_middleware

logger = Logger()

app = FastAPI()

FastAPIInstrumentor().instrument_app(app)


middleware = create_log_middleware(
    logger,
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
app.middleware("http")(middleware)


@app.get("/")
@traced()
def home():
    logger.info("Hello everyone")
    come_and_go()
    return


@traced()
def come_and_go():
    logger.info("I am good. How are you ?")
    return


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
