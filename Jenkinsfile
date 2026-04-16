@Library('my-first-shared-library@master') _

import java.util.UUID

pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "harshith0703/test-python"
        TAG = "${GIT_COMMIT}"

        PREVIEW_PORT = "5001"
        PROD_PORT = "5000"

        PREVIEW_URL = "http://localhost:5001"
        PROD_URL = "http://localhost:5000"

        APPROVAL_TOKEN = "${UUID.randomUUID().toString()}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git credentialsId: 'git',
                    url: 'https://github.com/harshith9xtech-hub/test.git',
                    branch: 'feature/ui'
            }
        }

        stage('Build Image') {
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
            steps {
                sh """
                    docker rm -f preview-app || true
                    docker run -d -p ${PREVIEW_PORT}:5000 \
                        --name preview-app \
                        ${DOCKER_IMAGE}:${TAG}
                """
            }
        }

        stage('Send Approval Email') {
            steps {
                script {

                    def approveUrl = "${env.BUILD_URL}input/Approve?token=${env.APPROVAL_TOKEN}"
                    def rejectUrl  = "${env.BUILD_URL}input/Reject?token=${env.APPROVAL_TOKEN}"

                    emailext(
                        to: "harshith.9xtech@gmail.com",
                        subject: "🚀 Deployment Approval Required - ${env.JOB_NAME}",
                        body: """
                        Feature build is ready.

                        Preview URL:
                        ${PREVIEW_URL}

                        Approve Deployment:
                        ${approveUrl}

                        Reject Deployment:
                        ${rejectUrl}

                        Jenkins:
                        ${env.BUILD_URL}
                        """
                    )
                }
            }
        }

        stage('Wait for Approval') {
            steps {
                input message: "Approve deployment to production?"
            }
        }

        stage('Push Image') {
            steps {
                sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${DOCKER_IMAGE}:${TAG}
                """
            }
        }

        stage('Deploy Production') {
            steps {
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
            emailext(
                to: "harshith.9xtech@gmail.com",
                subject: "Build Completed - ${currentBuild.currentResult}",
                body: """
                Status: ${currentBuild.currentResult}

                Preview: ${PREVIEW_URL}
                Production: ${PROD_URL}

                Jenkins: ${env.BUILD_URL}
                """
            )

            sh "docker image prune -f"
        }
    }
}
