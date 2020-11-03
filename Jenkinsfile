pipeline {
    agent none
    environment{
        BRANCH_NAME = "${env.BRANCH_NAME}"
        SANITIZED_BRANCH_NAME = "${env.BRANCH_NAME}".replace("/", "_")
        IMAGE_TAG = "${SANITIZED_BRANCH_NAME}"

        IMAGE_NAME = "ondewo-t2s-batch-server"
        TESTS_IMAGE_NAME = "ondewo-t2s-tests"
        TTS_NAME = "${IMAGE_NAME}:${IMAGE_TAG}"
        PUSH_NAME_STREAM = "dockerregistry.ondewo.com:5000/${TTS_NAME}"
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
                    environment {
                        ssh_key_file = credentials('devops_ondewo_idrsa')
                    }
                    steps {
                        sh(script: """set +x
                            docker build -t ${PUSH_NAME_STREAM} --build-arg SSH_PRIVATE_KEY=\"\$(cat ${ssh_key_file})\" --no-cache --target uncythonized -f docker/Dockerfile.batchserver .
                            set -x"""
                            , label: "build image"
                        )

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
                        sh(script: "docker build -t ${TESTS_IMAGE_NAME} --build-arg SSH_PRIVATE_KEY=\"\$(cat ${ssh_key_file})\" -f docker/Dockerfile.tests .", label: "build image")
                        sh(script: "docker run --rm -e TESTFILE=${testresults_filename} -v ${testresults_folder}:/opt/ondewo-t2s/log  ${TESTS_IMAGE_NAME}", label: "run_tests")
                     }
                     post { always {
                        sh(script: "cd ${testresults_folder} && cp *.xml ${PWD}")
                        junit "${testresults_filename}"
                     } }
                }
                stage('Push') { steps{
                        sh(script: "docker push ${PUSH_NAME_STREAM}", label: "push the image to the registry")
                        sh(script: "echo ${PUSH_NAME_STREAM} pushed to registry")
                } }
        } }
} }
