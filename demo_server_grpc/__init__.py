from demo_server_grpc.demo_utils import FileRemovalThread
from demo_server_grpc import routes
import os
from flask import Flask
from ondewologging.logger import logger_console as logger

server = Flask(__name__)

TMP_DIR_NAME: str = "tmp"
WORK_DIR: str = f"demo_server_grpc/{TMP_DIR_NAME}/"
if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

DEMO_URL: str = os.getenv("DEMO_URL", default="")
if not DEMO_URL:
    raise EnvironmentError("No DEMO_URL environmental variable found. "
                           "Please set the DEMO_URL variable. "
                           "For local development, the DEMO_URL should be set to "
                           "http://0.0.0.0:40040")
GRPC_HOST: str = os.getenv("GRPC_HOST", default="")
if not GRPC_HOST:
    raise EnvironmentError("No GRPC_HOST environmental variable found. "
                           "Please set this variable to the host of the T2S server. "
                           "For local development, the GRPC_HOST should be set to "
                           "http://0.0.0.0 or localhost")
GRPC_PORT: str = os.getenv("GRPC_PORT", default="")
if not GRPC_PORT:
    raise EnvironmentError("No GRPC_PORT environmental variable found. "
                           "Please set this variable to the port of the T2S server. "
                           "For local development, port is usually set to 50002")

# ===============================

file_removal_thread = FileRemovalThread()
file_removal_thread.start()
