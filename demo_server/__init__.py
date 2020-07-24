from demo_server import routes
import os
from flask import Flask

server = Flask(__name__)

WORK_DIR = "demo_server/tmp/"
if not os.path.isdir(WORK_DIR):
    os.mkdir(WORK_DIR)


# ===============================

if __name__ == '__main__':
    server.run()
