pipeline {
    agent any

    environment {
        // Static Webex Room ID
        WEBEX_ROOM_ID = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODEyNDA3NDAtY2Q1ZC0xMWYwLWFkMjctMmY0ZWY5NzZiMjIy' 
        // Variable for status tracking
        BUILD_STATUS = 'UNKNOWN' 
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Checking out source code...'
                checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/amanimaran14/devops-final-assignment.git']]])
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

    // --- Declarative Post Actions (Runs regardless of Stage 3 outcome) ---
    post {
        always {
            node('') {
                script {
                    echo "--- Stage 4. Webex Notification ---"
                    def finalStatus = currentBuild.result ?: 'ABORTED'
                    echo "Sending Webex notification with status: ${finalStatus}"
                    
                    withCredentials([string(credentialsId: 'WEBEX_BOT_TOKEN', variable: 'BOT_TOKEN')]) {
                        // THIS IS THE CORRECT LINE: It uses ${PWD} to mount the workspace.
                        sh "docker run --rm " +
                            "-v ${PWD}:/usr/src/app " +      // Mounts workspace contents to /usr/src/app
                            "-w /usr/src/app " +            // Sets container's working directory to /usr/src/app
                            "-e BUILD_URL=${env.BUILD_URL} " +
                            "-e WEBEX_ROOM_ID=${env.WEBEX_ROOM_ID} " +
                            "-e WEBEX_BOT_TOKEN=${BOT_TOKEN} " +
                            "code-quality-checker:latest python3 webex_notify.py ${finalStatus}"
                    }
                }
            }
        }
    }
}
