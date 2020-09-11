SHELL=/bin/bash
include .env
export

run_triton:
	-docker rm -f triton-inference-server
	docker run -d --rm --shm-size=1g --gpus all --ulimit memlock=-1 \
	--ulimit stack=67108864 --network=host --restart always \
	-v${PWD}/acoustic_models/triton_model_repository:/models \
	--name triton-inference-server ${IMAGE_NAME_TRITON} \
	tritonserver --model-repository=/models --api-version=2

run_batch_server_release:
	-docker kill ${CONTAINER_NAME}
	-docker rm ${CONTAINER_NAME}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host --restart always \
	-v ${PWD}/models:/opt/ondewo-t2s/models \
	-v ${PWD}/config:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/ondewo_t2s_config.yaml" \
	--name ${CONTAINER_NAME} \
	${IMAGE_NAME}
