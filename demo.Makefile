IMAGE_TAG_BATCH="dockerregistry.ondewo.com:5000/ondewo-t2s-batch-server:develop"
IMAGE_TAG_DEMO="dockerregistry.ondewo.com:5000/ondewo-t2s-demo-server:develop"
DEMO_CONTAINER="ondewo-t2s-demo-server"
BATCH_CONTAINER_DE="ondewo-t2s-batch-server-german"
BATCH_CONTAINER_EN="ondewo-t2s-batch-server-english"
PORT_DEMO=40040
PORT_DE=40041
PORT_EN=40042


build_demo_server:
	docker build -t ${IMAGE_TAG_DEMO} -f docker/Dockerfile.demoserver .

run_demo_server_locally:
	-docker rm -f ${DEMO_CONTAINER}
	docker run -td --rm \
	--network=host \
	--env DEMO_URL=http://0.0.0.0:${PORT_DEMO} \
	--env BATCH_DE_URL=http://0.0.0.0:${PORT_DE} \
	--env BATCH_EN_URL=http://0.0.0.0:${PORT_EN} \
	-v ${PWD}/config:/opt/ondewo-t2s/config \
	--name ${DEMO_CONTAINER} ${IMAGE_TAG_DEMO}

run_demo_server_production:
	-docker rm -f ${DEMO_CONTAINER}
	docker run -td --rm \
	--network=host \
	--env DEMO_URL="https://stella.s2t.demo.ondewo.com" \
	--env BATCH_DE_URL=http://0.0.0.0:${PORT_DE} \
	--env BATCH_EN_URL=http://0.0.0.0:${PORT_EN} \
	-v ${PWD}/config:/opt/ondewo-t2s/config \
	--name ${DEMO_CONTAINER} ${IMAGE_TAG_DEMO}

kill_all:
	-docker rm -f ${DEMO_CONTAINER}
	-docker rm -f ${BATCH_CONTAINER_DE}
	-docker rm -f ${BATCH_CONTAINER_EN}

run_servers: run_german_batch_server run_english_batch_server

run_german_batch_server:
	-docker rm -f ${BATCH_CONTAINER_DE}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${PWD}/models:/opt/ondewo-t2s/models \
	-v ${PWD}/config:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/demo/german_batch_server.yaml" \
	--name ${BATCH_CONTAINER_DE} \
	${IMAGE_TAG_BATCH} flask run --host=0.0.0.0 --port=${PORT_DE}

run_english_batch_server:
	-docker rm -f ${BATCH_CONTAINER_EN}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${PWD}/models:/opt/ondewo-t2s/models \
	-v ${PWD}/config:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/demo/english_batch_server.yaml" \
	--name ${BATCH_CONTAINER_EN} \
	${IMAGE_TAG_BATCH} flask run --host=0.0.0.0 --port=${PORT_EN}
