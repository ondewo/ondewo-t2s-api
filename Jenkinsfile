def UNIQUE_BUILD_ID = UUID.randomUUID().toString()

pipeline {
    agent none
    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
        SANITIZED_BRANCH_NAME = "${env.BRANCH_NAME}".replace('/', '-').replace('.', '-')
        IMAGE_TAG = "${SANITIZED_BRANCH_NAME}"

        IMAGE_NAME_REST = 'ondewo-t2s-rest-server'
        IMAGE_NAME_GRPC = 'ondewo-t2s-grpc-server'
        IMAGE_NAME_TESTS = 'ondewo-t2s-tests'
        IMAGE_NAME_CODE_CHECK = 'ondewo-t2s-code-check'

        TTS_NAME_REST = "${IMAGE_NAME_REST}:${IMAGE_TAG}"
        TTS_NAME_GRPC = "${IMAGE_NAME_GRPC}:${IMAGE_TAG}"
        TTS_NAME_TESTS = "${IMAGE_NAME_TESTS}:${IMAGE_TAG}"
        TTS_NAME_CODE_CHECK = "${IMAGE_NAME_CODE_CHECK}:${IMAGE_TAG}"
        PUSH_NAME_STREAM_REST = "dockerregistry.ondewo.com:5000/${TTS_NAME_REST}"
        PUSH_NAME_STREAM_GRPC = "dockerregistry.ondewo.com:5000/${TTS_NAME_GRPC}"
    }

    stages {
        stage('Code Quality Check') {
            agent { label 'cpu' }
            steps {
                sh(script: "docker build -t ${TTS_NAME_CODE_CHECK} -f code_checks/Dockerfile .", label: 'build code quality image')
                sh(script: "docker run --rm ${TTS_NAME_CODE_CHECK} make flake8", label: 'run flake8')
                sh(script: "docker run --rm ${TTS_NAME_CODE_CHECK} make mypy", label: 'run mypy')
            }
        }

        stage('Build and Test Server Images (uncythonized)') {
            agent { label 'gpu' }
            environment {
                ssh_key_file = credentials('devops_ondewo_idrsa')
                TRITON_CONTAINER = "ondewo-t2s-triton-${UNIQUE_BUILD_ID}"
                REST_CONTAINER = "${IMAGE_NAME_REST}-${UNIQUE_BUILD_ID}"
                GRPC_CONTAINER = "${IMAGE_NAME_GRPC}-${UNIQUE_BUILD_ID}"
                MODEL_REPO = 'models.ondewo.com:/raid/jenkins/data/t2s/models/'
                MODEL_DIR = '/mnt/disks/jenkins/data/t2s/models'
                TRITON_GPU = 'device=0'
                DOCKER_NETWORK = "${UNIQUE_BUILD_ID}"
            }
            stages {
                stage('Setup Test Env') {
                    steps {
                        sh(script: "mkdir -p ${MODEL_DIR}", label: 'create local cache dir')
                        sh(script: "rsync -Pavz ${MODEL_REPO} ${MODEL_DIR}", label: 'sync model repo to local cache dir')
                        sh(script: '''for filename in $(ls ${PWD}/tests/resources | grep yaml)
                                    do
                                        full_fp=${PWD}/tests/resources/\$filename
                                        sed -i "s/triton_url.*/triton_url: ${TRITON_CONTAINER}:50511/" \$full_fp
                                    done
                        ''', label: 'set triton container name in test configs')
                    }
                }
                stage('Build Server Images') {
                    stages { // NOTE: this is sequential (instead of parallel) as to not use too much GPU memory
                        stage('Build rest server') {
                            steps {
                                sh(script: """set +x
                                    docker build -t ${PUSH_NAME_STREAM_REST} --build-arg SSH_PRIVATE_KEY=\"\$(cat ${ssh_key_file})\" --target uncythonized -f docker/Dockerfile.rest_server .
                                    set -x"""
                                    , label: 'build image'
                                )
                            }
                        }
                        stage('Build grpc server') {
                            steps {
                                sh(script: """set +x
                                    docker build -t ${PUSH_NAME_STREAM_GRPC} --build-arg SSH_PRIVATE_KEY=\"\$(cat ${ssh_key_file})\" --target uncythonized -f docker/Dockerfile.grpc_server .
                                    set -x"""
                                    , label: 'build image'
                                )
                            }
                        }
                    }
                }
                stage('Build and Run Tests') {
                    environment {
                        PWD = pwd()
                        CONFIG_DIR = "${PWD}/tests/resources/configs"
                        testresults_folder = "${PWD}/test_results"
                        testresults_filename = 'pytest.xml'
                    }
                    stages {
                        stage('Build Test Image') {
                            steps {
                                sh(script: "mkdir ${testresults_folder}")
                                sh(script: "docker build -t ${TTS_NAME_TESTS} --build-arg PUSH_NAME_STREAM=\"${PUSH_NAME_STREAM_GRPC}\" -f docker/Dockerfile.tests .", label: 'build image')
                                sh(script: "docker network create ${DOCKER_NETWORK}", label: 'create docker network')
                            }
                        }
                        stage('Run Tests') {
                            parallel {
                                stage('Unit Tests') {
                                    steps {
                                        sh(script: "docker run --rm -e TESTFILE=${testresults_filename} -v ${testresults_folder}:/opt/ondewo-t2s/log ${TTS_NAME_TESTS} ./tests/unit"
                                        , label: 'run unit_tests')
                                    }
                                }
                                stage('Integration Tests') {
                                    steps {
                                        sh(script: "make run_triton TRITON_CONTAINER=${TRITON_CONTAINER} MODEL_DIR=${MODEL_DIR} TRITON_GPUS=\"${TRITON_GPU}\" DOCKER_NETWORK=${DOCKER_NETWORK}"
                                        , label: 'run triton server')
                                        timeout(time: 60, unit: 'SECONDS') {
                                            waitUntil {
                                                script {
                                                    def status_triton = sh(
                                                        script: "docker run --network=${DOCKER_NETWORK} dockerregistry.ondewo.com:5000/curlimages/curl curl --fail http://${TRITON_CONTAINER}:50510/v2/health/ready",
                                                        returnStatus: true,
                                                        label: 'health check triton until ready'
                                                    )
                                                    return (status_triton == 0)
                                                }
                                            }
                                        }
                                        sh(script: "docker logs ${TRITON_CONTAINER}", label: 'triton logs when ready')
                                        sh(script: """docker run --rm --gpus all \
                                            --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
                                            --network=${DOCKER_NETWORK} \
                                            -e TESTFILE=${testresults_filename} \
                                            -v ${testresults_folder}:/opt/ondewo-t2s/log \
                                            -v ${MODEL_DIR}:/opt/ondewo-t2s/models \
                                            ${TTS_NAME_TESTS} ./tests/integration"""
                                        , label: 'run integration tests')
                                    }
                                    post { always {
                                        sh(script: "docker logs ${TRITON_CONTAINER}", label: 'triton logs after tests')
                                        sh(script: 'make kill_triton'
                                        , label: 'kill triton server')
                                    } }
                                }
                                stage('E2E Tests') {
                                    steps {
                                        sh(script: """docker run -td --gpus all \
                                            --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
                                            --network=${DOCKER_NETWORK} \
                                            -v ${MODEL_DIR}:/opt/ondewo-t2s/models \
                                            -v ${CONFIG_DIR}:/opt/ondewo-t2s/config \
                                            --env CONFIG_FILE="config/config.yaml" \
                                            --env CUSTOM_PHOMENIZER_DIR="config/custom_phonemizers" \
                                            --name ${REST_CONTAINER} \
                                            ${PUSH_NAME_STREAM_REST}"""
                                        , label: 'run rest server')
                                        sh(script: """docker run -td --gpus all \
                                            --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
                                            --network=${DOCKER_NETWORK} \
                                            -v ${MODEL_DIR}:/opt/ondewo-t2s/models \
                                            -v ${CONFIG_DIR}:/opt/ondewo-t2s/config \
                                            --env CONFIG_DIR="config" \
                                            --name ${GRPC_CONTAINER} \
                                            ${PUSH_NAME_STREAM_GRPC}"""
                                        , label: 'run grpc server')
                                        timeout(time: 60, unit: 'SECONDS') {
                                            waitUntil {
                                                script {
                                                    def status_rest = sh(
                                                        script: "docker run --network=${DOCKER_NETWORK} dockerregistry.ondewo.com:5000/curlimages/curl curl --fail http://${REST_CONTAINER}:50550/health/ready",
                                                        returnStatus: true,
                                                        label: 'health check rest server until ready'
                                                    )
                                                    def status_grpc = sh(
                                                        script: "docker run --network=${DOCKER_NETWORK} dockerregistry.ondewo.com:5000/networld/grpcurl ./grpcurl -plaintext -H \"\" ${GRPC_CONTAINER}:50555 list",
                                                        returnStatus: true,
                                                        label: 'health check grpc server until ready'
                                                    )
                                                    return (status_rest + status_grpc == 0)
                                                }
                                            }
                                        }
                                        sh(script: "docker logs ${REST_CONTAINER}", label: 'rest server logs when ready')
                                        sh(script: "docker logs ${GRPC_CONTAINER}", label: 'grpc server logs when ready')
                                        sh(script: """docker run --rm --gpus all \
                                            --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
                                            --network=${DOCKER_NETWORK} \
                                            -e TESTFILE=${testresults_filename} \
                                            -e T2S_GRPC_HOST=${GRPC_CONTAINER} \
                                            -e T2S_REST_HOST=${REST_CONTAINER} \
                                            -v ${testresults_folder}:/opt/ondewo-t2s/log \
                                            -v ${MODEL_DIR}:/opt/ondewo-t2s/models \
                                            ${TTS_NAME_TESTS} ./tests/e2e"""
                                        , label: 'run e2e tests')
                                    }
                                    post { always {
                                        sh(script: "docker logs ${REST_CONTAINER}", label: 'rest server logs after tests')
                                        sh(script: "docker rm -f ${REST_CONTAINER}", label: 'kill rest server')
                                        sh(script: "docker logs ${GRPC_CONTAINER}", label: 'grpc server logs after tests')
                                        sh(script: "docker rm -f ${GRPC_CONTAINER}", label: 'kill grpc server')
                                    } }
                                }
                            }
                        }
                    }
                    post { always {
                        sh "docker network rm ${DOCKER_NETWORK} || exit 0"
                        sh(script: "cd ${testresults_folder} && cp *.xml ${PWD}")
                        junit "${testresults_filename}"
                    } }
                }
                stage('Push') {
                    steps {
                        sh(script: "docker push ${PUSH_NAME_STREAM_GRPC}", label: 'push the image to the registry')
                        sh(script: "echo ${PUSH_NAME_STREAM_GRPC} pushed to registry")
                        sh(script: "docker push ${PUSH_NAME_STREAM_REST}", label: 'push the image to the registry')
                        sh(script: "echo ${PUSH_NAME_STREAM_REST} pushed to registry")
                    }
                }
            }
        }
    }
}
