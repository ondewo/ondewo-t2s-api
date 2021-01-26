import os

T2S_REST_HOST = os.getenv("T2S_REST_HOST", "localhost")
T2S_REST_PORT = os.getenv("T2S_REST_PORT", "50550")
CHANNEL = f"{T2S_REST_HOST}:{T2S_REST_PORT}"
