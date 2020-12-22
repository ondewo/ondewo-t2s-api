import os

E2E_RESOURCES_PATH: str = os.path.join('tests', 'e2e', 'ressources')
CAI_HOST = os.getenv("CAI_HOST", "localhost")
CAI_GRPC_HOST = os.getenv("CAI_GRPC_HOST", "localhost")
CAI_GRPC_PORT = os.getenv("CAI_GRPC_PORT", "50002")
CHANNEL = f"{CAI_GRPC_HOST}:{CAI_GRPC_PORT}"
