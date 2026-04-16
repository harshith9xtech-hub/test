@Library('my-first-shared-library@master') _

pipeline {
    agent any

    environment {
        REPO = "test-python"
        DOCKER_IMAGE = "harshith0703/test-python"
        TAG = "${GIT_COMMIT}"
        PREVIEW_PORT = "5001"
        PROD_PORT = "5000"
        PREVIEW_URL = "http://localhost:5001"
        PROD_URL = "http://localhost:5000"
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
                    docker rm -f preview-app || true

                    docker run -d -p ${PREVIEW_PORT}:5000 \
                        --name preview-app \
                        ${DOCKER_IMAGE}:${TAG}

                    echo "Preview URL: ${PREVIEW_URL}"
                """
            }
        }

        stage('Send Approval Email') {
            steps {
                emailext(
                    subject: "🚀 Feature Build Ready - ${env.JOB_NAME}",
                    body: """
                    Build is ready for approval.

                    Preview URL:
                    ${PREVIEW_URL}

                    Approve in Jenkins:
                    ${env.BUILD_URL}
                    """,
                    to: "harshith.9xtech@gmail.com"
                )
            }
        }

        stage('Tester Approval') {
            steps {
                input message: "Approve deployment to production?"
            }
        }

        stage('Push Image') {
            steps {
                sh """
                    echo "Logging in..."
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                    echo "Pushing image..."
                    docker push ${DOCKER_IMAGE}:${TAG}
                """
            }
        }

        stage('Deploy Production (Localhost)') {
            steps {
                sh """
                    docker pull ${DOCKER_IMAGE}:${TAG}

                    docker rm -f prod-app || true

                    docker run -d -p ${PROD_PORT}:5000 \
                        --name prod-app \
                        ${DOCKER_IMAGE}:${TAG}

                    echo "Production URL: ${PROD_URL}"
                """
            }
        }
    }

    post {
        always {
            emailext(
                subject: "📦 Build Completed - ${env.JOB_NAME}",
                body: """
                Build Status: ${currentBuild.currentResult}

                Preview: ${PREVIEW_URL}
                Production: ${PROD_URL}

                Jenkins: ${env.BUILD_URL}
                """,
                to: "harshith.9xtech@gmail.com"
            )

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
