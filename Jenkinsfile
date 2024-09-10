pipeline {
    agent any
    environment {
        CONTAINER_NAME = "git-stats-container-${BUILD_NUMBER}"
    }
    stages {
        stage('[GIT] 🔍 Checkout') {
            steps {
                checkout scm
            }
        }
        stage('[DOCKER] 🐳 Run git-quick-stats') {
            steps {
                script {
                    // Start a long-running container
                    sh """
                        docker run -d --name ${CONTAINER_NAME} \
                            -v ${WORKSPACE}:/workspace \
                            alpine/git:latest \
                            tail -f /dev/null
                    """
                    
                    // Install git-quick-stats and run commands
                    sh """
                        docker exec ${CONTAINER_NAME} sh -c '
                            cd /workspace && \
                            wget -O /usr/local/bin/git-quick-stats https://raw.githubusercontent.com/arzzen/git-quick-stats/master/git-quick-stats && \
                            chmod +x /usr/local/bin/git-quick-stats && \
                            git-quick-stats -T > git-stats-output.txt && \
                            echo "\\n=== Detailed Report ===" >> git-stats-output.txt && \
                            git-quick-stats -R >> git-stats-output.txt && \
                            echo "\\n=== Commit Activity by Hour ===" >> git-stats-output.txt && \
                            git-quick-stats -c >> git-stats-output.txt && \
                            echo "\\n=== Commit Activity by Day ===" >> git-stats-output.txt && \
                            git-quick-stats -b >> git-stats-output.txt && \
                            echo "\\n=== List of Authors ===" >> git-stats-output.txt && \
                            git-quick-stats -D >> git-stats-output.txt
                        '
                    """
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'git-stats-output.txt', fingerprint: true
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }
        stage('[VALENTIN] 🛠️ Build') {
            steps {
                dir('server/client/valentin') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
        stage('[VALENTIN] 💅 Code formatting') {
           steps {
                dir('server/client/valentin') {
                    sh 'npm install prettier --save-dev'
                    sh 'npx prettier --check "**/*.{js,jsx,ts,tsx,json,css,scss,md}"'
                }
            }
            post {
                failure {
                    echo 'run: npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,scss,md}" to fix'
                }
            }
        }
    }
}
