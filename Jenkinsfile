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

        stage('Checkout Code') {
            steps {
                git credentialsId: 'git',
                    url: 'https://github.com/harshith9xtech-hub/test.git',
                    branch: 'feature/ui'
            }
        }

        stage('SonarQube Scan') {
            steps {
                sonar()
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

        stage('Deploy Preview (Localhost)') {
            steps {
                sh """
                    echo "Stopping old preview..."
                    docker rm -f preview-app || true

                    echo "Starting preview on localhost..."
                    docker run -d -p ${PREVIEW_PORT}:5000 \
                        --name preview-app \
                        ${DOCKER_IMAGE}:${TAG}

                    echo "Preview URL:"
                    echo "http://localhost:${PREVIEW_PORT}"
                """
            }
        }

        stage('Tester Approval (Manual)') {
            steps {
                input message: "Approve deployment to production?"
            }
        }

        stage('Send Approval Email (optional)') {
            steps {
                emailext (
                    subject: "🚀 Deployment Ready - ${env.JOB_NAME}",
                    body: """
                        Build Ready for Production

                        Preview URL:
                        http://localhost:${PREVIEW_PORT}

                        Click Jenkins for approval:
                        ${env.BUILD_URL}
                    """,
                    to: "harshith.9xtech@gmail.com"
                )
            }
        }

        stage('Push Image to Registry') {
            steps {
                sh """
                    echo "Logging into Docker Hub..."
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                    echo "Pushing image..."
                    docker push ${DOCKER_IMAGE}:${TAG}
                """
            }
        }

        stage('Deploy Production (Localhost)') {
            steps {
                input message: "Deploy to PRODUCTION on localhost?"

                sh """
                    docker pull ${DOCKER_IMAGE}:${TAG}

                    docker rm -f prod-app || true

                    docker run -d -p ${PROD_PORT}:5000 \
                        --name prod-app \
                        ${DOCKER_IMAGE}:${TAG}

                    echo "Production URL:"
                    echo "http://localhost:${PROD_PORT}"
                """
            }
        }
    }

    post {
        always {
            echo "Cleaning Docker..."
            sh "docker image prune -f"
        }

        success {
            echo "SUCCESS 🚀"
        }

        failure {
            echo "FAILED ❌"
        }
    }
}
