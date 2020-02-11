#!/bin/bash
cd /opt/stella/server/demo_server
export FLASK_APP=s2t_server.py
flask run --host=0.0.0.0
