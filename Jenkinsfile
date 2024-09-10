pipeline {
    agent any
    stages {
        stage('[GIT] 🔍 Checkout') {
            steps {
                checkout scm
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
        stage('[VALENTIN] 🔬 SonarQube Analysis') {
            steps {
                dir('server/client/valentin') {
                    withSonarQubeEnv('SonarQube') {  // Stellen Sie sicher, dass dieser Name mit Ihrer SonarQube-Serverkonfiguration in Jenkins übereinstimmt
                        sh """
                            ${SCANNER_HOME}/bin/sonar-scanner \
                            -Dsonar.projectKey=valentin-project \
                            -Dsonar.sources=. \
                            -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info \
                            -Dsonar.exclusions=**/node_modules/**,**/*.spec.ts
                        """
                    }
                }
            }
        }
        stage('[VALENTIN] ⏳ Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}
