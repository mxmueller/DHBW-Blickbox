pipeline {
    agent any
    stages {
        stage('[GIT] 🔍 Checkout') {
            steps {
                checkout scm
            }
        }
        stage('[DOCKER] 🐳 Build and Run git-quick-stats') {
            steps {
                script {
                    // Write Dockerfile content
                    def dockerfileContent = '''
                        FROM alpine:latest
                        RUN apk add --no-cache git bash curl wget
                        RUN wget -O /usr/local/bin/git-quick-stats https://raw.githubusercontent.com/arzzen/git-quick-stats/master/git-quick-stats && \
                            chmod +x /usr/local/bin/git-quick-stats
                        WORKDIR /repo
                        COPY . .
                        CMD ["sh", "-c", "git-quick-stats -T && git-quick-stats -R && git-quick-stats -c && git-quick-stats -b && git-quick-stats -D"]
                    '''
                    
                    // Write Dockerfile
                    writeFile file: 'Dockerfile', text: dockerfileContent
                    
                    // Build Docker image
                    sh 'docker build -t git-quick-stats-image .'
                    
                    // Run Docker container and capture output
                    sh '''
                        docker run --rm git-quick-stats-image | tee git-stats-output.txt
                    '''
                    
                    // Archive the output file
                    archiveArtifacts artifacts: 'git-stats-output.txt', fingerprint: true
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
    post {
        always {
            // Clean up: remove the Dockerfile and Docker image
            sh '''
                rm -f Dockerfile
                docker rmi git-quick-stats-image || true
            '''
        }
    }
}
