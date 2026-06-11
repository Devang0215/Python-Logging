from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

FastAPIInstrumentor(app)


@app.get("/")
def home():
    return "<h1>Hello, Flask!</h1><p>This is my first web application.</p>"


if __name__ == "__main__":
    app.run(debug=True)