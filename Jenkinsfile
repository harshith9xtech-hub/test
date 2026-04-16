@Library('my-first-shared-library@master') _

pipeline {
    agent any

    environment {
        REPO = "test-python"
        DOCKER_IMAGE = "harshith0703/test-python"
        TAG = "${GIT_COMMIT}"   // IMPORTANT: immutable artifact
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
                    branch: env.BRANCH_NAME
            }
        }

        stage('SonarQube Scan (Code Quality)') {
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

        stage('Trivy Scan (Security Gate)') {
            steps {
                trivyScan()
            }
        }

        stage('Deploy Preview (Feature Branch)') {
            when {
                expression { env.BRANCH_NAME.startsWith("feature/") }
            }
            steps {
                script {
                    sh """
                        echo "Stopping old preview container..."
                        docker rm -f preview-app || true

                        echo "Starting preview container..."
                        docker run -d -p ${PREVIEW_PORT}:5000 \
                        --name preview-app \
                        ${DOCKER_IMAGE}:${TAG}

                        docker ps
                    """
                }
            }
        }

        stage('Tester Approval') {
            when {
                expression { env.BRANCH_NAME.startsWith("feature/") }
            }
            steps {
                input message: "Approve this feature build for staging/production?"
            }
        }

        stage('Push Image to Docker Hub') {
            when {
                expression { env.BRANCH_NAME.startsWith("feature/") }
            }
            steps {
                pushImage()
            }
        }

        stage('Deploy Production (Master Only)') {
            when {
                branch 'master'
            }
            steps {
                input message: "Deploy to PRODUCTION?"

                script {
                    sh """
                        echo "Pulling image..."
                        docker pull ${DOCKER_IMAGE}:${TAG}

                        echo "Stopping old production container..."
                        docker rm -f prod-app || true

                        echo "Starting production container..."
                        docker run -d -p ${PROD_PORT}:5000 \
                        --name prod-app \
                        ${DOCKER_IMAGE}:${TAG}

                        docker ps
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline SUCCESS — Build, Scan, Deploy completed!"
        }

        failure {
            echo "❌ Pipeline FAILED — Check logs (Sonar/Trivy likely blocked it)"
        }

        always {
            echo "📊 Archiving Trivy report if exists..."
            archiveArtifacts artifacts: 'trivy-report.html', allowEmptyArchive: true

            echo "🧹 Cleaning unused Docker images..."
            sh 'docker image prune -f'
        }
    }
}
