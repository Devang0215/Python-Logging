import logging

from fastapi import FastAPI

app =FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@app.get("/home")
def home():
    value = False

    if value:
        logger.warning("\t This is a warning message")
    else:
        logger.error("\t This is an error message")
    return {"message": "Welcome to the home page!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)