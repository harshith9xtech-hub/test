pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "harshith0703/test-python"
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/harshith9xtech-hub/test.git', branch: "${env.BRANCH_NAME}"
            }
        }

        stage('Generate Report') {
            steps {
                sh """
                    echo "=====================================" > build-report.txt
                    echo " 🚀 BUILD REPORT " >> build-report.txt
                    echo "=====================================" >> build-report.txt
                    echo "Build Number : ${env.BUILD_NUMBER}" >> build-report.txt
                    echo "Job Name     : ${env.JOB_NAME}" >> build-report.txt
                    echo "Branch       : ${env.BRANCH_NAME}" >> build-report.txt
                    echo "Workspace    : ${env.WORKSPACE}" >> build-report.txt
                    echo "Build URL    : ${env.BUILD_URL}" >> build-report.txt
                    echo "Docker Image : ${DOCKER_IMAGE}" >> build-report.txt
                    echo "Image Tag    : ${TAG}" >> build-report.txt
                    echo "Build Time   : \$(date)" >> build-report.txt

                    echo "" >> build-report.txt
                    echo "🔀 Git Information:" >> build-report.txt
                    echo "Branch       : \$(git rev-parse --abbrev-ref HEAD)" >> build-report.txt
                    echo "Commit ID    : \$(git rev-parse HEAD)" >> build-report.txt
                    echo "Short Commit : \$(git rev-parse --short HEAD)" >> build-report.txt
                    echo "Last Commit  : \$(git log -1 --pretty=format:'%an - %s (%ci)')" >> build-report.txt

                    echo "" >> build-report.txt
                    echo "📦 System Versions:" >> build-report.txt
                    git --version >> build-report.txt
                    docker --version >> build-report.txt
                    python3 --version >> build-report.txt

                    echo "" >> build-report.txt
                    echo "📂 Files in Workspace:" >> build-report.txt
                    ls -l >> build-report.txt

                    echo "" >> build-report.txt
                    echo "=====================================" >> build-report.txt
                    echo "Build Completed Successfully ✅" >> build-report.txt
                    echo "=====================================" >> build-report.txt

                    cat build-report.txt
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$TAG .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh """
                    docker push $DOCKER_IMAGE:$TAG
                    docker tag $DOCKER_IMAGE:$TAG $DOCKER_IMAGE:latest
                    docker push $DOCKER_IMAGE:latest
                """
            }
        }

        stage('Deploy Container') {
            steps {
                sh """
                    docker stop python-app || true
                    docker rm python-app || true
                    docker run -d -p 5000:5000 --name python-app $DOCKER_IMAGE:$TAG
                """
            }
        }
    }

    post {
        success {
            echo "✅ Build SUCCESS: Image pushed & app deployed!"
            archiveArtifacts artifacts: 'build-report.txt'
        }

        failure {
            echo "❌ Build FAILED: Something went wrong!"
        }

        always {
            sh 'docker system prune -f'
        }
    }
}
