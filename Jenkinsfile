pipeline {
    agent any
    stages {
        stage('[GIT] 🔍 Checkout') {
            steps {
                checkout scm
            }
        }
        stage('[GIT] 🔍 Install git-quick-stats') {
            steps {
                sh '''
                    # Install git-quick-stats
                    sudo wget -O /usr/local/bin/git-quick-stats https://raw.githubusercontent.com/arzzen/git-quick-stats/master/git-quick-stats
                    sudo chmod +x /usr/local/bin/git-quick-stats
                '''
            }
        }

        stage('[GIT] 🔍 Run git-quick-stats') {
            steps {
                sh '''
                    echo "=== General Statistics ==="
                    git-quick-stats -T
                    
                    echo "\n=== Detailed Report ==="
                    git-quick-stats -R
                    
                    echo "\n=== Commit Activity by Hour ==="
                    git-quick-stats -c
                    
                    echo "\n=== Commit Activity by Day ==="
                    git-quick-stats -b
                    
                    echo "\n=== List of Authors ==="
                    git-quick-stats -D
                '''
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
        stage('[VALENTIN] 💅 Code formating') {
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
