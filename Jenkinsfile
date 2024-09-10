pipeline {
    agent any
    
    environment {
        CONTAINER_NAME = "git-stats-container-${BUILD_NUMBER}"
    }
    
    parameters {
        string(name: 'COMPOSE_FILE_1', defaultValue: 'docker-compose.yml', description: 'Pfad zur ersten Docker Compose-Datei')
        string(name: 'COMPOSE_FILE_2', defaultValue: 'docker-compose.override.yml', description: 'Pfad zur zweiten Docker Compose-Datei')
        string(name: 'COMPOSE_FILE_3', defaultValue: 'docker-compose.prod.yml', description: 'Pfad zur dritten Docker Compose-Datei')
    }

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
                    sh 'npx prettier --check "**/*.{js,jsx,ts,tsx,json,css,scss,md}"'
                }
            }
            post {
                failure {
                    echo 'run: npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,scss,md}" to fix'
                }
            }
        }
        
        stage('Install Docker Tools') {
            steps {
                sh '''
                    which hadolint || (curl -sL -o /usr/local/bin/hadolint https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64 && chmod +x /usr/local/bin/hadolint)
                    which yamllint || pip install yamllint
                '''
            }
        }
        
        stage('Lint Dockerfiles') {
            steps {
                script {
                    def dockerfiles = sh(script: 'find . -name Dockerfile -o -name "Dockerfile.*"', returnStdout: true).trim().split('\n')
                    dockerfiles.each { dockerfile ->
                        echo "Linting Dockerfile: ${dockerfile}"
                        sh "hadolint ${dockerfile}"
                    }
                }
            }
        }
        
        stage('Lint Docker Compose Files') {
            steps {
                script {
                    def composeFiles = [params.COMPOSE_FILE_1, params.COMPOSE_FILE_2, params.COMPOSE_FILE_3]
                    composeFiles.each { composeFile ->
                        if (fileExists(composeFile)) {
                            echo "Linting Docker Compose file: ${composeFile}"
                            sh "yamllint ${composeFile}"
                            sh "docker-compose -f ${composeFile} config -q"
                        } else {
                            echo "Warnung: Die Datei ${composeFile} existiert nicht und wird übersprungen."
                        }
                    }
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline fehlgeschlagen. Überprüfen Sie die Logs für Details zu Linting-Fehlern, Build-Problemen oder Formattierungsproblemen.'
        }
        success {
            echo 'Alle Überprüfungen, Builds und Linting-Prozesse erfolgreich abgeschlossen.'
        }
    }
}
