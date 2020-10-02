FROM python:3.7 AS py37_base

WORKDIR /ondewo/


COPY grpc_config_server/requirements.txt grpc_config_server/requirements.txt
RUN pip install -r grpc_config_server/requirements.txt

COPY grpc_config_server grpc_config_server
# COPY models models
COPY config config

CMD python -m grpc_config_server.tts_servicer

