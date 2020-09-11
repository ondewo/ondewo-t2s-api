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
                stage('Build') { steps {
                        sh(script: "docker build -t ${PUSH_NAME_STREAM} --target uncythonized -f docker/Dockerfile.batchserver .", label: "build image")
                } }
                stage('Tests') { steps {
                        sh(script: "docker build -t ${TESTS_IMAGE_NAME} -f docker/Dockerfile.tests .", label: "build image")
                        sh(script: "docker run --rm ${TESTS_IMAGE_NAME}", label: "run_tests")
                } }
                stage('Push') { steps{
                        sh(script: "docker push ${PUSH_NAME_STREAM}", label: "push the image to the registry")
                        sh(script: "echo ${PUSH_NAME_STREAM} pushed to registry")
                } }
        } }
} }
