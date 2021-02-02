import os

E2E_RESOURCES_PATH: str = os.path.join('tests', 'e2e', 'ressources')
T2S_HOST = os.getenv("T2S_HOST", "localhost")
T2S_GRPC_HOST = os.getenv("T2S_GRPC_HOST", "localhost")
T2S_GRPC_PORT = os.getenv("T2S_GRPC_PORT", "50555")
CHANNEL = f"{T2S_GRPC_HOST}:{T2S_GRPC_PORT}"
