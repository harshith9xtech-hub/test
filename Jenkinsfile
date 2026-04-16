@Library('my-first-shared-library@master') _

pipeline {
    agent any

    environment {
        REPO = "test-python"
        DOCKER_IMAGE = "harshith0703/test-python"
        TAG = "${env.GIT_COMMIT}"
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
                    echo "Stopping old preview container..."
                    docker rm -f preview-app || true

                    echo "Starting preview container..."
                    docker run -d -p ${PREVIEW_PORT}:5000 \
                        --name preview-app \
                        ${DOCKER_IMAGE}:${TAG}

                    echo "Preview URL:"
                    echo "http://localhost:${PREVIEW_PORT}"
                """
            }
        }

        stage('Send Approval Email') {
            steps {
                emailext (
                    subject: "🚀 Approval Required - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        Build is ready for production approval.

                        🔹 Preview URL:
                        http://localhost:${PREVIEW_PORT}

                        🔹 Jenkins Approval Link:
                        ${env.BUILD_URL}

                        Please open Jenkins and approve deployment.
                    """,
                    to: "harshith.9xtech@gmail.com"
                )
            }
        }

        stage('Tester Approval') {
            steps {
                input message: "Approve deployment to PRODUCTION?"
            }
        }

        stage('Push Image to Docker Hub') {
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
                sh """
                    echo "Pulling latest image..."
                    docker pull ${DOCKER_IMAGE}:${TAG}

                    echo "Stopping old production container..."
                    docker rm -f prod-app || true

                    echo "Starting production container..."
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
            echo "🧹 Cleaning Docker images..."
            sh "docker image prune -f"
        }

        success {
            echo "✅ SUCCESS - Deployment completed"
        }

        failure {
            echo "❌ FAILED - Check logs"
        }
    }
}
