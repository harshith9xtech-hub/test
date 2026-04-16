@Library('my-first-shared-library@master') _

pipeline {
    agent any

    environment {
        REPO = "test-python"
        DOCKER_IMAGE = "harshith0703/test-python"
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

                script {
                    // SAFE + RELIABLE TAG (fixes GIT_COMMIT issues)
                    env.TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
            }
        }

        stage('SonarQube Scan') {
            steps {
                sonar()
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds',
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    sh """
                        echo $PASS | docker login -u $USER --password-stdin
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    echo "Building Docker image..."
                    docker build -t ${DOCKER_IMAGE}:${TAG} .
                """
            }
        }

        stage('Trivy Scan (Security Gate)') {
            steps {
                sh """
                    docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    ghcr.io/aquasecurity/trivy:latest image \
                    --scanners vuln \
                    --severity HIGH,CRITICAL \
                    --exit-code 0 \
                    ${DOCKER_IMAGE}:${TAG}
                """
            }
        }

        stage('Deploy Preview (Feature Branch)') {
            when {
                expression { env.BRANCH_NAME?.startsWith("feature/") }
            }
            steps {
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

        stage('Tester Approval') {
            when {
                expression { env.BRANCH_NAME?.startsWith("feature/") }
            }
            steps {
                input message: "Approve this feature build for staging/production?"
            }
        }

        stage('Push Image to Docker Hub') {
            when {
                expression { env.BRANCH_NAME?.startsWith("feature/") }
            }
            steps {
                sh """
                    echo "Pushing image..."
                    docker push ${DOCKER_IMAGE}:${TAG}
                """
            }
        }

        stage('Deploy Production (Master Only)') {
            when {
                branch 'master'
            }
            steps {
                input message: "Deploy to PRODUCTION?"

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

    post {
        success {
            echo "✅ Pipeline SUCCESS — Build, Scan, Deploy completed!"
        }

        failure {
            echo "❌ Pipeline FAILED — Check logs (Sonar/Trivy/Docker issues)"
        }

        always {
            echo "📊 Archiving Trivy report if exists..."
            archiveArtifacts artifacts: 'trivy-report.html', allowEmptyArchive: true

            echo "🧹 Cleaning unused Docker images..."
            sh 'docker image prune -f'
        }
    }
}
