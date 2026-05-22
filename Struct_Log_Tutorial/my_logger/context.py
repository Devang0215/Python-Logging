import uuid
import structlog

def bind_request_context(user_id= None):

    request_id = str(uuid.uuid4())

    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        user_id=user_id
    ) 

    return request_id

def clear_request_context():
    structlog.contextvars.clear_contextvars()
    