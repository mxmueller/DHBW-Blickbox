pipeline {
    agent any
    stages {
        stage('[GIT] 🔍 Checkout') {
            steps {
                checkout scm
            }
        }
        stage('[GIT] 🕵️ GitLeaks Scan') {
            steps {
                sh '''
                    wget https://github.com/zricethezav/gitleaks/releases/download/v8.16.3/gitleaks_8.16.3_linux_x64.tar.gz
                    tar -xzf gitleaks_8.16.3_linux_x64.tar.gz
                    chmod +x gitleaks
                    ./gitleaks detect --source . -v --report-path gitleaks-report.json
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gitleaks-report.json', fingerprint: true
                }
                failure {
                    echo 'GitLeaks hat möglicherweise sensitive Daten gefunden. Bitte überprüfen Sie den Bericht.'
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
                    sh 'npx prettier --check "**/*.{js,jsx,ts,tsx,css,scss,md}"'
                }
            }
            post {
                failure {
                    echo 'run: npx prettier --write "**/*.{js,jsx,ts,tsx,css,scss,md}" to fix'
                }
            }
        }
        
        stage('[VALENTIN] 🧪 Jest Tests') {
            steps {
                dir('server/client/valentin') {
                    sh 'npm test'
                }
            }
            post {
                failure {
                    echo 'Jest tests failed. Please check the test results for more information.'
                }
            }
        }
        
        stage('[VALENTIN] 🛡️ Code Security Check') {
            steps {
                dir('server/client/valentin') {
                    sh 'npm install retire --save-dev'
                    sh 'npx retire --path . --outputformat json --outputpath ./retire-results.json'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'server/client/valentin/retire-results.json', fingerprint: true
                }
                failure {
                    echo 'Retire.js hat veraltete Bibliotheken mit bekannten Schwachstellen gefunden. Bitte überprüfen Sie den Bericht.'
                }
            }
        }
    }
}
