pipeline {
    agent any

    environment {
        WEBEX_ROOM_ID = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODEyNDA3NDAtY2Q1ZC0xMWYwLWFkMjctMmY0ZWY5NzZiMjIy'
    }

    stages {
        stage('1. Checkout Code & Fix Permissions') {
            steps {
                echo 'Checking out source code...'
                checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/amanimaran14/devops-final-assignment.git']]] )
                
                echo 'Fixing permissions on webex_notify.py'
                sh 'chmod +x webex_notify.py'
            }
        }

        stage('2. Build Checker Docker Image') {
            steps {
                script {
                    echo 'Building Docker image with Flake8 and app files included...'
                    docker.build("code-quality-checker:latest", "-f Dockerfile .")
                }
            }
        }

        stage('3. Run Flake8 Quality Check') {
            steps {
                script {
                    def flakeOutput = ''
                    try {
                        echo 'Running Flake8 inside Docker container...'
                        flakeOutput = docker.image("code-quality-checker:latest").inside {
                            sh(script: 'flake8 sample_app.py || true', returnStdout: true).trim()
                        }
                        if (flakeOutput) {
                            currentBuild.result = 'FAILURE'
                            echo "Flake8 issues found:\n${flakeOutput}"
                        } else {
                            currentBuild.result = 'SUCCESS'
                            echo "No Flake8 issues found."
                        }
                    } catch (e) {
                        currentBuild.result = 'FAILURE'
                        echo "Error running Flake8."
                        throw e
                    }
                    // Save output to environment variable for post stage
                    env.FLAKE8_OUTPUT = flakeOutput
                }
            }
        }
    }

    post {
        always {
            script {
                def finalStatus = currentBuild.currentResult ?: 'FAILURE'
                echo "--- Stage 4. Webex Notification ---"
                echo "Sending Webex notification with final status: ${finalStatus}"

                withCredentials([string(credentialsId: 'WEBEX_BOT_TOKEN', variable: 'WEBEX_BOT_TOKEN')]) {
                    docker.image("code-quality-checker:latest").inside(
                        "-e WEBEX_BOT_TOKEN=${WEBEX_BOT_TOKEN} " +
                        "-e WEBEX_ROOM_ID=${WEBEX_ROOM_ID} " +
                        "-e BUILD_URL=${BUILD_URL} " +
                        "-e FLAKE8_OUTPUT='${env.FLAKE8_OUTPUT}'"
                    ) {
                        sh "python3 webex_notify.py '${finalStatus}'"
                    }
                }
            }
        }
    }
}

