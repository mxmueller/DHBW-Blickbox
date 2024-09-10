pipeline {
    agent any
    stages {
        stage('[GIT] 🔍 Checkout') {
            steps {
                checkout scm
            }
        }
        stage('[DOCKER] 🐳 Run git-quick-stats') {
            agent {
                docker {
                    image 'alpine/git:latest'
                    args '-v ${WORKSPACE}:/workspace:rw'
                    reuseNode true
                }
            }
            steps {
                script {
                    sh '''
                        cd /workspace
                        wget -O /usr/local/bin/git-quick-stats https://raw.githubusercontent.com/arzzen/git-quick-stats/master/git-quick-stats
                        chmod +x /usr/local/bin/git-quick-stats
                        git-quick-stats -T > git-stats-output.txt
                        echo "\n=== Detailed Report ===" >> git-stats-output.txt
                        git-quick-stats -R >> git-stats-output.txt
                        echo "\n=== Commit Activity by Hour ===" >> git-stats-output.txt
                        git-quick-stats -c >> git-stats-output.txt
                        echo "\n=== Commit Activity by Day ===" >> git-stats-output.txt
                        git-quick-stats -b >> git-stats-output.txt
                        echo "\n=== List of Authors ===" >> git-stats-output.txt
                        git-quick-stats -D >> git-stats-output.txt
                    '''
                }
            }
            post {
                success {
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
}
