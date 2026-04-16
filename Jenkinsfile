@Library('my-first-shared-library@master') _
pipeline {
    agent any
     environment {
        REPO = "test-python"
        TAG = "${env.BUILD_NUMBER}"
        PORT = "5001"
        DOCKER_IMAGE = "harshith0703/test-python"
    }
    stages{
        stage('Share-library-message'){
         steps{
             simpleEcho()
         }
        }
        stage('git-checkout'){
            steps{
                git credentialsId: 'git',
                url: 'https://github.com/harshith9xtech-hub/test.git'
            }
        }
        stage('docker-login'){
            steps{
                dockerLogin(credentialsId: 'docker-hub-creds')
            }
        }
        stage('docker'){
            steps{
                buildImage()
            }
        }
        stage('deploy'){
            steps{
                deployApp()
            }
        }
    }
}
