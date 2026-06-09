import random
import time
import uuid
from typing import List

from fastapi import FastAPI, HTTPException, Query
from my_logger import create_span, get_logger, logging_middleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel

app = FastAPI(title="Sample FastAPI Application", version="1.0.0")

FastAPIInstrumentor.instrument_app(app)
app.middleware("http")(logging_middleware)

logger = get_logger()

class User(BaseModel):
    id: str | None = None
    name: str
    email: str


class Product(BaseModel):
    id: str | None = None
    name: str
    price: float


users = {}
products = {}


@app.get("/")
async def root():
    with create_span("root"):
        message = "Welcome to the Sample FastAPI Application with Structured Logging and OpenTelemetry!"
        logger.info("Root endpoint accessed", message=message)
    return {"message": "FastAPI Application Running"}


@app.get("/health")
async def health_check():
    message = {
        "status": "healthy",
        "service": "sample-api",
    }
    logger.info("Root endpoint accessed", message=message)
    check_done()
    return {"status": "healthy", "service": "sample-api"}

def check_done():
    logger.info("Checking if done")

@app.get("/slow")
async def slow_endpoint():
    """Simulates a slow request."""
    time.sleep(3)
    return {"message": "Slow endpoint completed"}


@app.get("/error")
async def error_endpoint():
    """Simulates an application error."""
    raise HTTPException(status_code=500, detail="Simulated Internal Server Error")


@app.post("/users", response_model=User)
async def create_user(user: User):
    user_id = str(uuid.uuid4())
    user.id = user_id
    users[user_id] = user
    return user


@app.get("/users", response_model=List[User])
async def get_users():
    return list(users.values())


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return users[user_id]


@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]

    return {"message": f"User {user_id} deleted successfully"}


@app.post("/products", response_model=Product)
async def create_product(product: Product):
    product_id = str(uuid.uuid4())
    product.id = product_id
    products[product_id] = product

    return product


@app.get("/products", response_model=List[Product])
async def get_products():
    return list(products.values())


@app.get("/products/{product_id}")
async def get_product(product_id: str):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    return products[product_id]


@app.get("/search")
async def search(keyword: str = Query(...), limit: int = Query(10, ge=1, le=100)):
    return {
        "keyword": keyword,
        "limit": limit,
        "results": [f"Result {i}" for i in range(1, limit + 1)],
    }


@app.get("/random-status")
async def random_status():
    status = random.choice(["success", "processing", "failed"])

    return {"status": status}


@app.get("/compute")
async def compute(number: int):
    result = number * number

    return {"input": number, "square": result}
