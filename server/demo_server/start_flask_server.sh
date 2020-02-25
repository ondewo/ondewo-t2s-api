#!/bin/bash
cd /opt/stella/server/demo_server
export FLASK_APP=t2s_server.py
flask run --host=0.0.0.0
