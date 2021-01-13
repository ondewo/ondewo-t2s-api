pipeline {
    agent none
    environment{
        BRANCH_NAME = "${env.BRANCH_NAME}"
        SANITIZED_BRANCH_NAME = "${env.BRANCH_NAME}".replace("/", "_")
        IMAGE_TAG = "${SANITIZED_BRANCH_NAME}"

        IMAGE_NAME = "ondewo-t2s"
        IMAGE_NAME_BATCH = "ondewo-t2s-batch-server"
        IMAGE_NAME_GRPC = "ondewo-t2s-grpc-server"
        TESTS_IMAGE_NAME = "ondewo-t2s-tests"
        TTS_NAME_BATCH = "${IMAGE_NAME_BATCH}:${IMAGE_TAG}"
        TTS_NAME_GRPC = "${IMAGE_NAME_GRPC}:${IMAGE_TAG}"
        PUSH_NAME_STREAM_BATCH = "dockerregistry.ondewo.com:5000/${TTS_NAME_BATCH}"
        PUSH_NAME_STREAM_GRPC = "dockerregistry.ondewo.com:5000/${TTS_NAME_GRPC}"
        test_IMAGE_NAME = "test_image_${IMAGE_NAME}"

        code_check_image_name = "code_check_image_${IMAGE_NAME}"
    }

    stages {
        stage('Code quality') { agent { label 'cpu' }
            steps {
                sh(script: "docker build -t ${code_check_image_name} -f code_checks/Dockerfile .", label: "build code quality image")
                sh(script: "docker run --rm ${code_check_image_name} make flake8", label: "run flake8")
                sh(script: "docker run --rm ${code_check_image_name} make mypy", label: "run mypy")
        } }

        stage('Normal image') { agent { label 'cpu' }
            stages{
                stage('Build') {
                    parallel{
                        stage('Build batch server'){
                            environment {
                                ssh_key_file = credentials('devops_ondewo_idrsa')
                            }
                            steps {
                                sh(script: """set +x
                                    docker build -t ${PUSH_NAME_STREAM_BATCH} --build-arg SSH_PRIVATE_KEY=\"\$(cat ${ssh_key_file})\" --target uncythonized -f docker/Dockerfile.batchserver .
                                    set -x"""
                                    , label: "build image"
                                )
                                }
                            }
                        stage('Build grpc server'){
                            environment {
                                ssh_key_file = credentials('devops_ondewo_idrsa')
                            }
                            steps {
                                sh(script: """set +x
                                    docker build -t ${PUSH_NAME_STREAM_GRPC} --build-arg SSH_PRIVATE_KEY=\"\$(cat ${ssh_key_file})\" --target uncythonized -f docker/Dockerfile.grpc_server .
                                    set -x"""
                                    , label: "build image"
                                )
                                }
                            }
                        }
                }
                stage('Tests') {
                     environment {
                        PWD = pwd()
                        testresults_folder = "${PWD}/test_results"
                        testresults_filename = "pytest.xml"
                        ssh_key_file = credentials('devops_ondewo_idrsa')
                     }
                     steps {
                        sh(script: "mkdir ${testresults_folder}")
                        sh(script: "docker build -t ${TESTS_IMAGE_NAME} --build-arg PUSH_NAME_STREAM=\"${PUSH_NAME_STREAM_GRPC}\" -f docker/Dockerfile.tests .", label: "build image")
                        sh(script: "docker run --rm -e TESTFILE=${testresults_filename} -v ${testresults_folder}:/opt/ondewo-t2s/log  ${TESTS_IMAGE_NAME} --ignore=tests/tests_grpc", label: "run_tests")
                     }
                     post { always {
                        sh(script: "cd ${testresults_folder} && cp *.xml ${PWD}")
                        junit "${testresults_filename}"
                     } }
                }
                stage('Push') { steps{
                        sh(script: "docker push ${PUSH_NAME_STREAM_GRPC}", label: "push the image to the registry")
                        sh(script: "echo ${PUSH_NAME_STREAM_GRPC} pushed to registry")
                        sh(script: "docker push ${PUSH_NAME_STREAM_BATCH}", label: "push the image to the registry")
                        sh(script: "echo ${PUSH_NAME_STREAM_BATCH} pushed to registry")
                } }
        } }
} }
