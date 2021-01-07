import os
from flask import Flask
from ondewologging.logger import logger_console as logger

server = Flask(__name__)

TMP_DIR_NAME: str = "tmp"
WORK_DIR: str = f"demo_server/{TMP_DIR_NAME}/"
if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

DEMO_URL: str = os.getenv("DEMO_URL", default="")
if not DEMO_URL:
    raise EnvironmentError("No DEMO_URL environmental variable found. "
                           "Please set the DEMO_URL variable. "
                           "For local development, the DEMO_URL should be set to "
                           "http://0.0.0.0:40040")
BATCH_DE_URL: str = os.getenv("BATCH_DE_URL", default="")
if not BATCH_DE_URL:
    raise EnvironmentError("No BATCH_DE_URL environmental variable found. "
                           "Please set this variable to the url of the T2S German "
                           "batch server.")
BATCH_EN_URL: str = os.getenv("BATCH_EN_URL", default="")
if not BATCH_EN_URL:
    raise EnvironmentError("No BATCH_EN_URL environmental variable found. "
                           "Please set this variable to the url of the T2S English "
                           "batch server.")

# ===============================
from demo_server import routes
from demo_server.demo_utils import FileRemovalThread

file_removal_thread = FileRemovalThread()
file_removal_thread.start()

