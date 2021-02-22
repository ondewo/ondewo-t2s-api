FROM registry-ci.ondewo.com:5000/python/python:3.7-slim

ENV HOST_IP=172.17.0.1
ENV LOCAL_MIRROR=http://"$HOST_IP":/3141/root/pypi/+simple/

RUN apt-get update && apt-get install make

RUN echo [global] >> /etc/pip.conf && \
    echo index-url = http://$HOST_IP:3141/root/pypi/+simple/ >> /etc/pip.conf && \
    echo [install] >> /etc/pip.conf && \
    echo trusted-host = $HOST_IP >> /etc/pip.conf && \
    echo "              pypi.org" >> /etc/pip.conf && \
    echo extra-index-url = https://pypi.org/simple/ >> /etc/pip.conf && \
    echo no-cache-dir = true >> /etc/pip.conf && \
    echo timeout = 100 >> /etc/pip.conf && \
    cat /etc/pip.conf && \
    pip install flake8 mypy

RUN mkdir code_to_test

WORKDIR code_to_test

ENV FOLDER_NAME=testcode
COPY grpc_server $FOLDER_NAME/grpc_server
COPY rest_server $FOLDER_NAME/rest_server
COPY demo_server $FOLDER_NAME/demo_server
COPY inference $FOLDER_NAME/inference
COPY normalization $FOLDER_NAME/normalization
COPY utils $FOLDER_NAME/utils
COPY tests $FOLDER_NAME/tests

COPY code_checks .
