IMAGE_TAG_GRPC="registry-dev.ondewo.com:5000/ondewo-t2s-grpc-server-release:develop"
IMAGE_TAG_DEMO="registry-dev.ondewo.com:5000/ondewo-t2s-demo-server:develop"
DEMO_CONTAINER="ondewo-t2s-demo-server"
GRPC_CONTAINER="ondewo-t2s-grpc-server"
PORT_DEMO=50540
PORT_GRPC=50555
HOST_GRPC="localhost"

build_demo_server: export SSH_PRIVATE_KEY="$$(cat ~/.ssh/id_rsa)"
build_demo_server:
	docker build -t ${IMAGE_TAG_DEMO} --build-arg SSH_PRIVATE_KEY=$(SSH_PRIVATE_KEY) -f docker/Dockerfile.demoserver .

run_demo_server_locally:
	-docker rm -f ${DEMO_CONTAINER}
	docker run -td --rm \
        --network=host \
        --env DEMO_URL=http://0.0.0.0:${PORT_DEMO} \
        --env GRPC_HOST=${HOST_GRPC} \
        --env GRPC_PORT=${PORT_GRPC} \
        -v ${PWD}/config:/opt/ondewo-t2s/config \
        --name ${DEMO_CONTAINER} ${IMAGE_TAG_DEMO}

run_demo_server_production:
	-docker rm -f ${DEMO_CONTAINER}
	docker run -td --rm \
        --network=host \
        --env DEMO_URL="https://t2s.demo.cloud.ondewo.com" \
        --env GRPC_HOST=${HOST_GRPC} \
        --env GRPC_PORT=${PORT_GRPC} \
        -v ${PWD}/config:/opt/ondewo-t2s/config \
        --name ${DEMO_CONTAINER} ${IMAGE_TAG_DEMO}

run_grpc_server:
	-docker kill ${GRPC_CONTAINER}
	-docker rm ${GRPC_CONTAINER}
	docker run -td --gpus all \
        --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
        --network=host \
        -v ${shell pwd}/models:/opt/ondewo-t2s/models \
        -v ${shell pwd}/config:/opt/ondewo-t2s/config \
        --env CONFIG_DIR="config" \
        --name ${GRPC_CONTAINER} \
        ${IMAGE_TAG_GRPC}

kill_all:
	-docker rm -f ${DEMO_CONTAINER}
	-docker rm -f ${GRPC_CONTAINER}
