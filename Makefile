DOCKERREGISTRY = "registry-dev.ondewo.com:5000"
NAMESPACE = "ondewo"
RELEASE_VERSION = "1.5.3"

IMAGE_TAG_REST="${DOCKERREGISTRY}/${NAMESPACE}/ondewo-t2s-rest-server:${RELEASE_VERSION}"
IMAGE_TAG_GRPC="${DOCKERREGISTRY}/${NAMESPACE}/ondewo-t2s-grpc-server:${RELEASE_VERSION}"
IMAGE_TAG_REST_RELEASE="${DOCKERREGISTRY}/${NAMESPACE}/ondewo-t2s-rest-server-release:${RELEASE_VERSION}"
IMAGE_TAG_GRPC_RELEASE="${DOCKERREGISTRY}/${NAMESPACE}/ondewo-t2s-grpc-server-release:${RELEASE_VERSION}"
IMAGE_TAG_TESTS="ondewo-t2s-tests-image"
IMAGE_TAG_TRITON="${DOCKERREGISTRY}/nvidia/tritonserver:20.09-py3"
IMAGE_TAG_CODE_CHECK="code_check_image"

REST_CONTAINER="ondewo-t2s-rest-server"
GRPC_CONTAINER="ondewo-t2s-grpc-server"
REST_CONTAINER_RELEASE="ondewo-t2s-rest-server-release"
GRPC_CONTAINER_RELEASE="ondewo-t2s-grpc-server-release"
TESTS_CONTAINER="ondewo-t2s-tests"
TRITON_CONTAINER ?="ondewo-t2s-triton-inference-server"

MODEL_DIR ?= "${shell pwd}/models"
CONFIG_DIR ?= "${shell pwd}/config"
TRITON_GPUS ?= "all"
DOCKER_NETWORK ?= "host"


### --- Build code checks image and run --- ###
run_code_checks:
	docker build -t ${IMAGE_TAG_CODE_CHECK} -f code_checks/Dockerfile .
	docker run --rm ${IMAGE_TAG_CODE_CHECK} make flake8
	docker run --rm ${IMAGE_TAG_CODE_CHECK} make mypy


### --- Image builds --- ###
build_rest_server: export SSH_PRIVATE_KEY="$$(cat ~/.ssh/id_rsa)"
build_rest_server:
	docker build -t ${IMAGE_TAG_REST} --build-arg SSH_PRIVATE_KEY=$(SSH_PRIVATE_KEY) --target uncythonized -f docker/Dockerfile.rest_server .

build_grpc_server: export SSH_PRIVATE_KEY="$$(cat ~/.ssh/id_rsa)"
build_grpc_server:
	docker build -t ${IMAGE_TAG_GRPC} --build-arg SSH_PRIVATE_KEY=$(SSH_PRIVATE_KEY) --target uncythonized -f docker/Dockerfile.grpc_server .

build_rest_server_release: export SSH_PRIVATE_KEY="$$(cat ~/.ssh/id_rsa)"
build_rest_server_release:
	docker build -t ${IMAGE_TAG_REST_RELEASE} --build-arg SSH_PRIVATE_KEY=$(SSH_PRIVATE_KEY) -f docker/Dockerfile.rest_server .

build_grpc_server_release: export SSH_PRIVATE_KEY="$$(cat ~/.ssh/id_rsa)"
build_grpc_server_release:
	docker build -t ${IMAGE_TAG_GRPC_RELEASE} --build-arg SSH_PRIVATE_KEY=$(SSH_PRIVATE_KEY) -f docker/Dockerfile.grpc_server .


### --- Run Triton --- ###
run_triton:
	-docker kill ${TRITON_CONTAINER}
	-docker rm ${TRITON_CONTAINER}
	docker run -d --shm-size=1g --gpus ${TRITON_GPUS} --ulimit memlock=-1 \
		--ulimit stack=67108864 --network=${DOCKER_NETWORK} \
		-v ${MODEL_DIR}/triton_repo:/models \
		--name ${TRITON_CONTAINER} ${IMAGE_TAG_TRITON} \
	tritonserver --model-repository=/models --strict-model-config=false \
		--log-verbose=1 --backend-config=tensorflow,version=2 \
		--grpc-port=50511 --http-port=50510

kill_triton:
	docker kill ${TRITON_CONTAINER}
	docker rm ${TRITON_CONTAINER}

run_triton_on_dgx:
	-kill -9 $(ps aux | grep "ssh -N -f -L localhost:50511:dgx:50511 voice_user@dgx"| grep -v grep| awk '{print $2}')
	ssh -N -f -L localhost:50511:dgx:50511 voice_user@dgx

stop_ssh_tunel:
	-kill -9 $(ps aux | grep "ssh -N -f -L localhost:50511:dgx:50511 voice_user@dgx"| grep -v grep| awk '{print $2}')


### --- Run Rest Server --- ###
run_rest_server:
	-docker kill ${REST_CONTAINER}
	-docker rm ${REST_CONTAINER}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=${DOCKER_NETWORK} \
	-v ${MODEL_DIR}:/opt/ondewo-t2s/models \
	-v ${CONFIG_DIR}:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/config.yaml" \
	--name ${REST_CONTAINER} \
	${IMAGE_TAG_REST}

run_rest_server_release:
	-docker kill ${REST_CONTAINER_RELEASE}
	-docker rm ${REST_CONTAINER_RELEASE}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=${DOCKER_NETWORK} \
	-v ${MODEL_DIR}:/opt/ondewo-t2s/models \
	-v ${CONFIG_DIR}:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/config.yaml" \
	--name ${REST_CONTAINER_RELEASE} \
	${IMAGE_TAG_REST_RELEASE}


### --- Run gRPC Server --- ###
run_grpc_server:
	-docker kill ${GRPC_CONTAINER}
	-docker rm ${GRPC_CONTAINER}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=${DOCKER_NETWORK} \
	-v ${MODEL_DIR}:/opt/ondewo-t2s/models \
	-v ${CONFIG_DIR}:/opt/ondewo-t2s/config \
	--env CONFIG_DIR="config" \
	--name ${GRPC_CONTAINER} \
	${IMAGE_TAG_GRPC}

run_grpc_server_release:
	-docker kill ${GRPC_CONTAINER_RELEASE}
	-docker rm ${GRPC_CONTAINER_RELEASE}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=${DOCKER_NETWORK} \
	-v ${MODEL_DIR}:/opt/ondewo-t2s/models \
	-v ${CONFIG_DIR}:/opt/ondewo-t2s/config \
	--env CONFIG_DIR="config" \
	--name ${GRPC_CONTAINER_RELEASE} \
	${IMAGE_TAG_GRPC_RELEASE}


### --- Run Tests --- ###
run_tests:  export SSH_PRIVATE_KEY="$$(cat ~/.ssh/id_rsa)"
run_tests:
	docker build -t ${IMAGE_TAG_TESTS} --build-arg PUSH_NAME_STREAM=${IMAGE_TAG_GRPC} -f docker/Dockerfile.tests .
	-docker rm -f ${TESTS_CONTAINER} \
	docker run --rm --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-e TESTFILE=pytest.xml \
	-v ${PWD}/test_results:/opt/ondewo-t2s/log \
	--name ${TESTS_CONTAINER} ${IMAGE_TAG_TESTS}


### --- Package Release --- ###
package_git_revision_and_version:
	echo "version: `cat utils/version.py | grep -oP "(?<=__version__ = ')(.*)(?=')"`" > package/VERSION.md
	echo "" >> package/VERSION.md
	echo "git revision: ` git rev-parse --short HEAD`" >> package/VERSION.md

package_release: package_git_revision_and_version
	echo "Who am I: `whoami`"
	echo "Where am I: `pwd`"
	echo "My environment variables: `env`"

	mkdir -p ${RELEASE_FOLDER}

	# tar and zip images
	docker pull ${PUSH_NAME_RELEASE_REST}
	docker pull ${PUSH_NAME_RELEASE_GRPC}
	docker save ${PUSH_NAME_RELEASE_REST} | gzip > ${RELEASE_FOLDER}/ondewo-t2s-rest-server-release-${SANITIZED_DOCKER_TAG_NAME}.tar.gz
	docker save ${PUSH_NAME_RELEASE_GRPC} | gzip > ${RELEASE_FOLDER}/ondewo-t2s-grpc-server-release-${SANITIZED_DOCKER_TAG_NAME}.tar.gz

	# add configs
	rsync -av config package --exclude demo

	# move package to the release folder
	rsync -av package/. ${RELEASE_FOLDER} --exclude '.gitignore'
	rm -rf package

	rsync -Pha ${RELEASE_FOLDER} ondewo@releases.ondewo.com:/mnt/disks/releases/ondewo-t2s


### --- Install dependencies locally --- ###
install_dependencies_locally: generate_ondewo_protos
	pip install nvidia-pyindex
	pip install -r requirements.txt

	-git clone git@bitbucket.org:ondewo/ondewo-t2s-glow.git
	cd ondewo-t2s-glow && git fetch && git checkout 176dd93688cfadc84c4996283cec518fec5a7830 && \
	cd monotonic_align && python setup.py build_ext --inplace
	pip install -e ondewo-t2s-glow

	-git clone git@bitbucket.org:ondewo/ondewo-t2s-hifigan.git
	cd ondewo-t2s-hifigan && git fetch && git checkout 1d691b8abc13275649be72809b681333bc47f1e6
	pip install -e ondewo-t2s-hifigan


# GENERATE PYTHON FILES FROM PROTOS
# copy from nlu-client, changed output directory to ./grpc_config_server/ and only exporting /audio/ directory of ondewoapis
ONDEWO_PROTOS_DIR=ondewo-t2s-api/ondewo/t2s
GOOGLE_APIS_DIR=ondewo-t2s-api/googleapis
ONDEWO_APIS_DIR=ondewo-t2s-api
PROTO_OUTPUT_FOLDER=ondewo_grpc

generate_ondewo_protos:
	mkdir -p ondewo_grpc
	for f in $$(find ${ONDEWO_PROTOS_DIR} -name '*.proto'); do \
		python -m grpc_tools.protoc -I ${ONDEWO_APIS_DIR} --python_out=${PROTO_OUTPUT_FOLDER} --mypy_out=${PROTO_OUTPUT_FOLDER} --grpc_python_out=${PROTO_OUTPUT_FOLDER} $$f; \
	done
	python utils/fix_imports.py -sp ${PROTO_OUTPUT_FOLDER} # fix imports into subdirectory


# to generate image of the server with models inside you need to specify arguments of the models and config paths
# do not forget to check .dockerignore file most likely the model dir is there you need to comment it out or delete
# the models dir should contain all the models (glow-tts and hifi) in separate dirs
# make sure that config has correct paths of trained model pth file and json file of glow-tts config
# same with hifi model
# Example of the generation command:
# make create_model_server_from_package RELEASE_VERSION=1.5.3 COMPANY=ondewo IMAGE_NAME=ondewo-t2s-model-german-kerstin\
 MODEL_DIR=models/atos/models CONFIG_PATH=models/atos/config/config.yaml
create_model_server_from_package:
	docker build -t ${DOCKERREGISTRY}/${COMPANY}/${IMAGE_NAME}:${RELEASE_VERSION} \
	--build-arg ONDEWO_T2S_SERVER=${IMAGE_TAG_GRPC_RELEASE} \
	--build-arg MODEL_DIR=${MODEL_DIR} \
   	--build-arg CONFIG_PATH=${CONFIG_PATH} \
    -f docker/models_with_server_package.Dockerfile .