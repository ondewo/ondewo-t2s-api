IMAGE_TAG_BATCH="dockerregistry.ondewo.com:5000/stella-batch-server"
IMAGE_TAG_BATCH="dockerregistry.ondewo.com:5000/stella-batch-server-release"
IMAGE_TAG_TRAINING="dockerregistry.ondewo.com:5000/stella-training"
BATCH_CONTAINER="stella-batch-server"
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
	docker build -t ${IMAGE_TAG_BATCH}  -f docker/Dockerfile.server .

build_training_image:
	docker build -t ${IMAGE_TAG_TRAINING} training

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
	-v ${PWD}/models:/opt/ondewo-s2t-stella/models \
	--restart always \
	--name ${SERVER_CONTAINER} \
	${IMAGE_TAG_BATCH}

install_dependencies_locally:
	pip install -r requirements.txt
	pip install utils/triton_client_lib/triton*.whl

