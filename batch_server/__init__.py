import os

from flask import Flask

from inference.inference import Inference
from inference.inference_factory import InferenceFactory
from utils.logger import logger

server = Flask(__name__)
server.logger.setLevel(logger)

WORK_DIR = "batch_server/tmp/"
if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

inference: Inference = InferenceFactory.get_inference("config/batch_server_config_triton.yaml")
# ===============================
from batch_server import routes

if __name__ == '__main__':
    server.run()
