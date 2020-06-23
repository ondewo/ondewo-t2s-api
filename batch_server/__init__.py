import os
from flask import Flask
import logging
from inference.nemo_inference import NemoInference

server = Flask(__name__)
server.logger.setLevel(logging.DEBUG)

WORK_DIR = "batch_server/tmp/"
if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)

inference = InferenceFactory("config/batch_server_config_nemo.yaml", logger=server.logger)
# ===============================
from batch_server import routes

if __name__ == '__main__':
    server.run()
