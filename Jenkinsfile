pipeline {
    agent none
    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
        SANITIZED_BRANCH_NAME = "${env.BRANCH_NAME}".replace('/', '_')
        IMAGE_TAG = "${SANITIZED_BRANCH_NAME}"

        IMAGE_NAME = 'ondewo-t2s'
        IMAGE_NAME_REST = 'ondewo-t2s-rest-server'
        IMAGE_NAME_GRPC = 'ondewo-t2s-grpc-server'
        TESTS_IMAGE_NAME = 'ondewo-t2s-tests'
        TTS_NAME_REST = "${IMAGE_NAME_REST}:${IMAGE_TAG}"
        TTS_NAME_GRPC = "${IMAGE_NAME_GRPC}:${IMAGE_TAG}"
        PUSH_NAME_STREAM_REST = "dockerregistry.ondewo.com:5000/${TTS_NAME_REST}"
        PUSH_NAME_STREAM_GRPC = "dockerregistry.ondewo.com:5000/${TTS_NAME_GRPC}"
        test_IMAGE_NAME = "test_image_${IMAGE_NAME}"

        code_check_image_name = "code_check_image_${IMAGE_NAME}"
        A100_MODEL_DIR = '/home/voice_user/data/jenkins/t2s/models'
    }

    stages {
        stage('Code Quality Check') {
            agent {
                label 'cpu'
            }
            steps {
                sh(script: "docker build -t ${code_check_image_name} -f code_checks/Dockerfile .", label: 'build code quality image')
                sh(script: "docker run --rm ${code_check_image_name} make flake8", label: 'run flake8')
                sh(script: "docker run --rm ${code_check_image_name} make mypy", label: 'run mypy')
            }
        }

        stage('Build and Test Server Images (uncythonized)') {
            agent {
                label 'a100'
            }
            environment {
                ssh_key_file = credentials('devops_ondewo_idrsa')
            }
            stages {
                stage('Build Server Images') {
                    parallel {
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
                        testresults_folder = "${PWD}/test_results"
                        testresults_filename = 'pytest.xml'
                    }
                    stages {
                        stage('Build Test Image') {
                            steps {
                                sh(script: "mkdir ${testresults_folder}")
                                sh(script: "docker build -t ${TESTS_IMAGE_NAME} --build-arg PUSH_NAME_STREAM=\"${PUSH_NAME_STREAM_GRPC}\" -f docker/Dockerfile.tests .", label: 'build image')
                            }
                        }
                        stage('Run Tests') {
                            // replace "stages" with "parallel" when tests become parallel
                            stages {
                                stage('Unit Tests') {
                                    steps {
                                        sh(script: "docker run --rm -e TESTFILE=${testresults_filename} -v ${testresults_folder}:/opt/ondewo-t2s/log ${TESTS_IMAGE_NAME} ./tests/unit"
                                        , label: 'run unit_tests')
                                    }
                                }
                                stage('Integration Tests') {
                                    steps {
                                        sh(script: "make run_triton MODEL_DIR=${A100_MODEL_DIR}"
                                        , label: 'run triton server')
                                        sh(script: "docker run --rm -e TESTFILE=${testresults_filename} -v ${testresults_folder}:/opt/ondewo-t2s/log -v ${A100_MODEL_DIR}:/opt/ondewo-t2s/models ${TESTS_IMAGE_NAME} ./tests/integration"
                                        , label: 'run integration tests')
                                    }
                                    post {
                                        always {
                                            sh(script: 'make kill_triton'
                                            , label: 'kill triton server')
                                        }
                                    }
                                }
                            }
                        }
                    }
                    post {
                        always {
                            sh(script: "cd ${testresults_folder} && cp *.xml ${PWD}")
                            junit "${testresults_filename}"
                        }
                    }
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
