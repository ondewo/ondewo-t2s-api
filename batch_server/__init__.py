import os
from flask import Flask
import logging
from inference.triton_inference import TritonInference

server = Flask(__name__)
server.logger.setLevel(logging.DEBUG)

WORK_DIR = "batch_server/tmp/"
if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

nemo_inference = TritonInference("config/batch_server_config_triton.yaml", logger=server.logger)
# ===============================
from batch_server import routes

if __name__ == '__main__':
    server.run()
