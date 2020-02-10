BASE_IMAGE_TAG="dockerregistry.ondewo.com:5000/pytorch:19.11-py3"
IMAGE_TAG="dockerregistry.ondewo.com:5000/nvidia-nemo-tts"
CONTAINER_NAME="local-t2s-server"

build_image:
	-docker kill ${CONTAINER_NAME}
	docker pull ${BASE_IMAGE_TAG}
	docker build -t ${IMAGE_TAG} .

run_container:
	docker run -t -d --gpus all --rm \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	-v ${PWD}:/opt/stella \
	-p 5003:5000 \
	--name ${CONTAINER_NAME} ${IMAGE_TAG}

