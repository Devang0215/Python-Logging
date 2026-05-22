import os

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

JSON_LOGS = os.getenv(
    "JSON_LOGS",
    "False"
).lower() == "true"