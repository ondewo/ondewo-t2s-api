IMAGE_TAG_REST="dockerregistry.ondewo.com:5000/ondewo-t2s-rest-server:develop"
IMAGE_TAG_GRPC="dockerregistry.ondewo.com:5000/ondewo-t2s-grpc-server:develop"
IMAGE_TAG_REST_RELEASE="dockerregistry.ondewo.com:5000/ondewo-t2s-rest-server-release:develop"
IMAGE_TAG_GRPC_RELEASE="dockerregistry.ondewo.com:5000/ondewo-t2s-grpc-server-release:develop"
IMAGE_TAG_TESTS="ondewo-t2s-tests-image"
IMAGE_TAG_TRITON="dockerregistry.ondewo.com:5000/nvidia/tritonserver:20.09-py3"
REST_CONTAINER="ondewo-t2s-rest-server"
GRPC_CONTAINER="ondewo-t2s-grpc-server"
REST_CONTAINER_RELEASE="ondewo-t2s-rest-server-release"
GRPC_CONTAINER_RELEASE="ondewo-t2s-grpc-server-release"
CODE_CHECK_IMAGE="code_check_image"
TESTS_CONTAINER="ondewo-t2s-tests"
GRPC_CONFIG_DIR ?= "config"


run_code_checks: ## Start the code checks image and run the checks
	docker build -t ${CODE_CHECK_IMAGE} -f code_checks/Dockerfile .
	docker run --rm ${CODE_CHECK_IMAGE} make flake8
	docker run --rm ${CODE_CHECK_IMAGE} make mypy

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

run_triton:
	-docker rm -f triton-inference-server
	docker run -d --shm-size=1g --gpus all --ulimit memlock=-1 \
		--ulimit stack=67108864 --network=host \
		-v${shell pwd}/models/triton_repo:/models \
		--name triton-inference-server ${IMAGE_TAG_TRITON} \
	tritonserver --model-repository=/models --strict-model-config=false \
		--log-verbose=1 --backend-config=tensorflow,version=2 \
		--grpc-port=50511 --http-port=50510

run_triton_on_dgx:
	-kill -9 $(ps aux | grep "ssh -N -f -L localhost:50511:dgx:50511 voice_user@dgx"| grep -v grep| awk '{print $2}')
	ssh -N -f -L localhost:50511:dgx:50511 voice_user@dgx

stop_ssh_tunel:
	-kill -9 $(ps aux | grep "ssh -N -f -L localhost:50511:dgx:50511 voice_user@dgx"| grep -v grep| awk '{print $2}')

run_rest_server:
	-docker kill ${REST_CONTAINER}
	-docker rm ${REST_CONTAINER}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${shell pwd}/models:/opt/ondewo-t2s/models \
	-v ${shell pwd}/config:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/config.yaml" \
	--name ${REST_CONTAINER} \
	${IMAGE_TAG_REST}

run_grpc_server:
	-docker kill ${GRPC_CONTAINER}
	-docker rm ${GRPC_CONTAINER}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${shell pwd}/models:/opt/ondewo-t2s/models \
	-v ${shell pwd}/config:/opt/ondewo-t2s/config \
	--env CONFIG_DIR=${GRPC_CONFIG_DIR} \
	--name ${GRPC_CONTAINER} \
	${IMAGE_TAG_GRPC}

run_rest_server_release:
	-docker kill ${REST_CONTAINER_RELEASE}
	-docker rm ${REST_CONTAINER_RELEASE}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${shell pwd}/models:/opt/ondewo-t2s/models \
	-v ${shell pwd}/config:/opt/ondewo-t2s/config \
	--env CONFIG_FILE="config/config.yaml" \
	--name ${REST_CONTAINER_RELEASE} \
	${IMAGE_TAG_REST_RELEASE}

run_grpc_server_release:
	-docker kill ${GRPC_CONTAINER_RELEASE}
	-docker rm ${GRPC_CONTAINER_RELEASE}
	docker run -td --gpus all \
	--shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
	--network=host \
	-v ${shell pwd}/models:/opt/ondewo-t2s/models \
	-v ${shell pwd}/config:/opt/ondewo-t2s/config \
	--env CONFIG_DIR="config" \
	--name ${GRPC_CONTAINER_RELEASE} \
	${IMAGE_TAG_GRPC_RELEASE}

run_tests:  export SSH_PRIVATE_KEY="$$(cat ~/.ssh/id_rsa)"
run_tests: build_rest_server
	docker build -t ${IMAGE_TAG_TESTS} --build-arg PUSH_NAME_STREAM=${IMAGE_TAG_REST} -f docker/Dockerfile.tests .
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

	mkdir -p ${RELEASE_FOLDER}

	# tar and zip images
	docker pull ${PUSH_NAME_RELEASE}
	docker save ${PUSH_NAME_RELEASE} | gzip > ${RELEASE_FOLDER}/ondewo-t2s-rest-server-release-${SANITIZED_DOCKER_TAG_NAME}.tar.gz

	# add configs
	rsync -av config package --exclude demo

	# move package to the release folder
	rsync -av package/. ${RELEASE_FOLDER} --exclude '.gitignore'
	rm -rf package

	rsync -Phaz ${RELEASE_FOLDER} ondewo@releases.ondewo.com:releases/ondewo-t2s

install_dependencies_locally: generate_ondewo_protos
	pip install nvidia-pyindex
	pip install -r requirements.txt

	-git clone git@bitbucket.org:ondewo/ondewo-t2s-glow.git
	cd ondewo-t2s-glow && git fetch && git checkout 588cb9946743f6eec85d0fe35b1e3395ea651a87 && \
	cd monotonic_align && python setup.py build_ext --inplace
	pip install -e ondewo-t2s-glow

	-git clone git@bitbucket.org:ondewo/ondewo-logging-python.git
	cd ondewo-logging-python && git pull
	pip install -e ondewo-logging-python

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

