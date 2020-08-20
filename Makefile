IMAGE_TAG_BATCH="dockerregistry.ondewo.com:5000/stella-batch-server:develop"
IMAGE_TAG_BATCH_RELEASE="dockerregistry.ondewo.com:5000/stella-batch-server-release:develop"
IMAGE_TAG_TRAINING="dockerregistry.ondewo.com:5000/stella-training"
BATCH_CONTAINER="stella-batch-server"
BATCH_CONTAINER_RELEASE="stella-batch-server-release"
TRAINING_CONTAINER="stella-training"
CODE_CHECK_IMAGE="code_check_image"
SERVER_PORT = 40015
TRAINING_PORT = 40011


run_code_checks: ## Start the code checks image and run the checks
	docker build -t ${CODE_CHECK_IMAGE} -f code_checks/Dockerfile .
	docker run --rm ${CODE_CHECK_IMAGE} make flake8
	docker run --rm ${CODE_CHECK_IMAGE} make mypy

build_batch_server:
	docker build -t ${IMAGE_TAG_BATCH} --target uncythonized -f docker/Dockerfile.batchserver .

build_batch_server_release:
	docker build -t ${IMAGE_TAG_BATCH_RELEASE}  -f docker/Dockerfile.batchserver .

build_training_image:
	docker build -t ${IMAGE_TAG_TRAINING} training

run_triton:
	docker pull nvcr.io/nvidia/tritonserver:20.03.1-py3
	-docker kill triton-inference-server
	docker run -d --rm --shm-size=1g --gpus all --ulimit memlock=-1 \
	--ulimit stack=67108864 --network=host \
	-v${PWD}/models/triton_repo:/models \
	--name triton-inference-server nvcr.io/nvidia/tritonserver:20.03.1-py3 \
	tritonserver --model-repository=/models --api-version=2 --strict-model-config=false

run_triton_on_aistation:
	-kill -9 $(ps aux | grep "ssh -N -f -L localhost:8001:aistation:8001 voice_user@aistation"| grep -v grep| awk '{print $2}')
	ssh -N -f -L localhost:8001:aistation:8001 voice_user@aistation

stop_ssh_tunel:
	-kill -9 $(ps aux | grep "ssh -N -f -L localhost:8001:aistation:8001 voice_user@aistation"| grep -v grep| awk '{print $2}')

run_training_container:
	-docker kill ${TRAINING_CONTAINER}
	-docker rm ${TRAINING_CONTAINER}
	docker run -t -d --gpus all --rm \
	--shm-size=10g --ulimit memlock=-1 --ulimit stack=67108864 \
	-v ${PWD}/models:/opt/models \
	-v ${PWD}/training:/opt/stella \
	-p ${TRAINING_PORT}:5000 \
	--name ${TRAINING_CONTAINER} ${IMAGE_TAG_TRAINING}

run_batch_server:
	-docker kill ${BATCH_CONTAINER}
	-docker rm ${BATCH_CONTAINER}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${PWD}/models:/opt/ondewo-t2s-stella/models \
	-v ${PWD}/config:/opt/ondewo-t2s-stella/config \
	--env CONFIG_FILE="config/stella_config.yaml" \
	--name ${BATCH_CONTAINER} \
	${IMAGE_TAG_BATCH}

run_batch_server_release:
	-docker kill ${BATCH_CONTAINER_RELEASE}
	-docker rm ${BATCH_CONTAINER_RELEASE}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${PWD}/models:/opt/ondewo-t2s-stella/models \
	-v ${PWD}/config:/opt/ondewo-t2s-stella/config \
	--env CONFIG_FILE="config/stella_config.yaml" \
	--name ${BATCH_CONTAINER_RELEASE} \
	${IMAGE_TAG_BATCH_RELEASE}

install_dependencies_locally:
	pip install -r requirements.txt
	pip install utils/triton_client_lib/triton*.whl

