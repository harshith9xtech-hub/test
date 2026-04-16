@Library('my-first-shared-library@master') _

pipeline {
    agent any

    environment {
        REPO = "test-python"
        DOCKER_IMAGE = "harshith0703/test-python"
        TAG = "${GIT_COMMIT}"
        PREVIEW_PORT = "5001"
        PROD_PORT = "5000"
    }

    stages {

        stage('Shared Library Check') {
            steps {
                simpleEcho()
            }
        }

        stage('Checkout Code') {
            steps {
                git credentialsId: 'git',
                    url: 'https://github.com/harshith9xtech-hub/test.git',
                    branch: 'main'
            }
        }

        stage('SonarQube Scan') {
            steps {
                sonar()
            }
        }

        stage('Docker Login') {
            steps {
                dockerLogin(credentialsId: 'docker-hub-creds')
            }
        }

        stage('Build Docker Image') {
            steps {
                buildImage()
            }
        }

        stage('Trivy Scan') {
            steps {
                trivyScan()
            }
        }

        stage('Deploy Preview') {
            when {
                expression { env.BRANCH_NAME?.startsWith("feature/") }
            }
            steps {
                sh """
                    docker rm -f preview-app || true
                    docker run -d -p ${PREVIEW_PORT}:5000 \
                    --name preview-app \
                    ${DOCKER_IMAGE}:${TAG}
                """
            }
        }

        stage('Tester Approval') {
            when {
                expression { env.BRANCH_NAME?.startsWith("feature/") }
            }
            steps {
                input message: "Approve this feature build for staging/production?"
            }
        }

        stage('Push Image') {
            when {
                expression { env.BRANCH_NAME?.startsWith("feature/") }
            }
            steps {
                pushImage()
            }
        }

        stage('Deploy Production') {
            when {
                branch 'master'
            }
            steps {
                input message: "Deploy to PRODUCTION?"

                sh """
                    docker pull ${DOCKER_IMAGE}:${TAG}
                    docker rm -f prod-app || true
                    docker run -d -p ${PROD_PORT}:5000 \
                    --name prod-app \
                    ${DOCKER_IMAGE}:${TAG}
                """
            }
        }
    }

    post {
        always {
            echo "Cleaning up..."
            sh "docker image prune -f"
        }

        success {
            echo "SUCCESS 🚀"
        }

        failure {
            echo "FAILED ❌ (check logs)"
        }
    }
}
