pipeline {
    agent any

    environment {
        // REPLACE THESE PLACEHOLDERS
        WEBEX_BOT_TOKEN = credentials('YzA2NmZkNDgtYzlhMS00ZjllLWEwZDEtYzYxN2UzYzcwNDY5YTg4YmRkZWYtN2Q4_P0A1_13494cac-24b4-4f89-8247-193cc92a7636')
        WEBEX_ROOM_ID = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODEyNDA3NDAtY2Q1ZC0xMWYwLWFkMjctMmY0ZWY5NzZiMjIy' 
        BUILD_STATUS = 'UNKNOWN' 
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Checking out source code...'
                // REPLACE THIS WITH YOUR REPO DETAILS
                git url: 'https://github.com/amanimaran14/devops-final-assignment.git', branch: 'main'
            }
        }

        stage('2. Build Checker Docker Image') {
            steps {
                script {
                    echo 'Building Docker image with Flake8...'
                    docker.build("code-quality-checker:latest", "-f Dockerfile .")
                }
            }
        }

        stage('3. Run Flake8 Quality Check') {
            steps {
                script {
                    try {
                        echo 'Running Flake8 inside the Docker container...'
                        docker.image("code-quality-checker:latest").inside {
                            sh 'flake8 ./sample_app.py' 
                        }
                        env.BUILD_STATUS = 'PASS'
                    } catch (e) {
                        env.BUILD_STATUS = 'FAIL'
                        echo "Flake8 check failed. Details in the build log."
                        throw e 
                    }
                }
            }
        }
    }

    post {
        always {
            stage('4. Webex Notification') {
                steps {
                    echo "Sending Webex notification with status: ${env.BUILD_STATUS}"
                    docker.image("code-quality-checker:latest").inside {
                        sh "python3 webex_notify.py ${env.BUILD_STATUS}"
                    }
                }
            }
        }
    }
}
