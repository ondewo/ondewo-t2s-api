# install grpcurl for grpc health check
FROM ubuntu:18.04 as lux_base

# install grpcurl
# docker.io needed for 'go get'
RUN apt update && apt install -y docker.io
RUN apt-get update && apt-get install -y golang
RUN go get github.com/fullstorydev/grpcurl/...
RUN go install github.com/fullstorydev/grpcurl/cmd/grpcurl

# install server
FROM ubuntu:18.04 as lux_base_next
COPY --from=lux_base /root/go/bin/ /usr/local/bin/

# install docker.io
RUN apt update && apt install -y docker.io

# install python
RUN apt-get update && apt-get upgrade -y && apt-get clean && \
    apt-get install -y curl python3.7 python3.7-dev python3.7-distutils && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1 && \
    update-alternatives --set python /usr/bin/python3.7 && \
    curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py --force-reinstall && \
    rm get-pip.py && \
    apt-get remove -y curl

WORKDIR /ondewo/

# install requirements
COPY grpc_config_server/requirements.txt grpc_config_server/requirements.txt
RUN pip install -r grpc_config_server/requirements.txt

# copy server code (./models and ./config is volume-mapped)
COPY grpc_config_server grpc_config_server


CMD python -m grpc_config_server.tts_server

# instantiate health check
EXPOSE 7777
HEALTHCHECK --interval=1s --timeout=3s \
  CMD grpcurl -plaintext -H "" localhost:7777 list || exit 1
