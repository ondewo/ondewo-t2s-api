SHELL=/bin/bash
include .env
export

install:
	gunzip -c ondewo-t2s-batch-server-release-${ONDEWO_T2S_VERSION}.tar.gz | docker load
	gunzip -c ondewo-t2s-grpc-server-release-${ONDEWO_T2S_VERSION}.tar.gz | docker load

run: run_rest_server_release

run_triton:
	-docker rm -f triton-inference-server
	docker run -d --rm --shm-size=1g --gpus all --ulimit memlock=-1 \
	--ulimit stack=67108864 --network=host --restart always \
	-v${shell pwd}/acoustic_models/triton_model_repository:/models \
	--name triton-inference-server ${IMAGE_NAME_TRITON} \
	tritonserver --model-repository=/models --api-version=2

run_rest_server_release:
	-docker kill ${CONTAINER_NAME_REST}
	-docker rm ${CONTAINER_NAME_REST}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host --restart always \
	-v ${shell pwd}/models:/opt/ondewo-t2s/models \
	-v ${shell pwd}/config:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/config.yaml" \
	--name ${CONTAINER_NAME_REST} \
	${IMAGE_NAME_REST}

run_grpc_server_release:
	-docker kill ${CONTAINER_NAME_GRPC}
	-docker rm ${CONTAINER_NAME_GRPC}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host --restart always \
	-v ${shell pwd}/models:/opt/ondewo-t2s/models \
	-v ${shell pwd}/config:/opt/ondewo-t2s/config \
	--env CONFIG_DIR="config" \
	--name ${CONTAINER_NAME_GRPC} \
	${IMAGE_NAME_GRPC}
