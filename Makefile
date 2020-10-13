IMAGE_TAG_BATCH="dockerregistry.ondewo.com:5000/ondewo-t2s-batch-server:develop"
IMAGE_TAG_BATCH_RELEASE="dockerregistry.ondewo.com:5000/ondewo-t2s-batch-server-release:develop"
IMAGE_TAG_TRAINING="dockerregistry.ondewo.com:5000/ondewo-t2s-training"
IMAGE_TAG_TESTS="ondewo-t2s-tests-image"
IMAGE_TAG_TRITON="nvcr.io/nvidia/tritonserver:20.08-py3"
BATCH_CONTAINER="ondewo-t2s-batch-server"
BATCH_CONTAINER_RELEASE="ondewo-t2s-batch-server-release"
TRAINING_CONTAINER="ondewo-t2s-training"
CODE_CHECK_IMAGE="code_check_image"
TESTS_CONTAINER="ondewo-t2s-tests"
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
	-docker rm -f triton-inference-server
	docker run -d --shm-size=1g --gpus all --ulimit memlock=-1 \
	--ulimit stack=67108864 --network=host \
	-v${shell pwd}/models/triton_repo:/models \
	--name triton-inference-server ${IMAGE_TAG_TRITON} \
	tritonserver --model-repository=/models --strict-model-config=false

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
	-v ${shell pwd}/models:/opt/models \
	-v ${shell pwd}/training:/opt/ondewo-t2s \
	-p ${TRAINING_PORT}:5000 \
	--name ${TRAINING_CONTAINER} ${IMAGE_TAG_TRAINING}

run_batch_server:
	-docker kill ${BATCH_CONTAINER}
	-docker rm ${BATCH_CONTAINER}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${shell pwd}/models:/opt/ondewo-t2s/models \
	-v ${shell pwd}/config:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/config.yaml" \
	--name ${BATCH_CONTAINER} \
	${IMAGE_TAG_BATCH}

run_batch_server_release:
	-docker kill ${BATCH_CONTAINER_RELEASE}
	-docker rm ${BATCH_CONTAINER_RELEASE}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${shell pwd}/models:/opt/ondewo-t2s/models \
	-v ${shell pwd}/config:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/config.yaml" \
	--name ${BATCH_CONTAINER_RELEASE} \
	${IMAGE_TAG_BATCH_RELEASE}

run_tests:
	docker build -t ${IMAGE_TAG_TESTS} -f docker/Dockerfile.tests .
	-docker rm -f ${TESTS_CONTAINER}
	docker run --rm -e TESTFILE=pytest.xml -v ${PWD}/test_results:/opt/ondewo-t2s/log \
	--name ${TESTS_CONTAINER} ${IMAGE_TAG_TESTS}

package_git_revision_and_version:
	echo "version: `cat utils/version.py | grep -oP "(?<=__version__ = ')(.*)(?=')"`" > package/VERSION.md
	echo "" >> package/VERSION.md
	echo "git revision: ` git rev-parse --short HEAD`" >> package/VERSION.md

make package_release: package_git_revision_and_version
	echo "Who am I: `whoami`"
	echo "Where am I: `pwd`"
	echo "My environment variables: `env`"

	mkdir -p ${RELEASE_FOLDER}/${SANITIZED_DOCKER_TAG_NAME}

	# tar and zip images
	docker save ${PUSH_NAME_RELEASE} | gzip > ${RELEASE_FOLDER}/${SANITIZED_DOCKER_TAG_NAME}/ondewo-t2s-batch-server-release-${SANITIZED_DOCKER_TAG_NAME}.tar.gz

	# add configs
	rsync -av config package --exclude demo

	# move to the release folder
	rsync -av package/. ${RELEASE_FOLDER}/${SANITIZED_DOCKER_TAG_NAME} --exclude '.gitignore'
	rm -rf package

install_dependencies_locally:
	pip install -r requirements.txt
	pip install utils/triton_client_lib/triton*.whl

# GENERATE PYTHON FILES FROM PROTOS
# copy from nlu-client, changed output directory to ./grpc_config_server/ and only exporting /audio/ directory of ondewoapis
ONDEWO_PROTOS_DIR=ondewoapis/ondewo/audio
GOOGLE_APIS_DIR=ondewoapis/googleapis
ONDEWO_APIS_DIR=ondewoapis
PROTO_OUTPUT_FOLDER=grpc_config_server/

generate_ondewo_protos:
	for f in $$(find ${ONDEWO_PROTOS_DIR} -name '*.proto'); do \
		python -m grpc_tools.protoc -I${GOOGLE_APIS_DIR} -I${ONDEWO_APIS_DIR} --python_out=${PROTO_OUTPUT_FOLDER} --mypy_out=${PROTO_OUTPUT_FOLDER} --grpc_python_out=${PROTO_OUTPUT_FOLDER} $$f; \
	done

build_grpc_server:
	# ignore dockerignore by moving it before the build, and restore it afterwards
	mkdir ignoreme
	mv .dockerignore ignoreme/.dockerignore # move away .dockerignore
	mv grpc_config_server/grpc_dockerignore .dockerignore
	docker build -t t2s_grpc_server -f grpc_config_server/Dockerfile .
	mv .dockerignore grpc_config_server/grpc_dockerignore
	mv ignoreme/.dockerignore .dockerignore # restore .dockerignore
	rm -r ignoreme

run_grpc_server:
	docker-compose -f grpc_config_server/docker-compose.yaml up

remove_grpc_exited_container:
	docker-compose -f grpc_config_server/docker-compose.yaml rm -f

