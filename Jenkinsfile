pipeline {
    agent any
    
    parameters {
        string(name: 'COMPOSE', defaultValue: 'docker-compose.yaml')
        string(name: 'COMPOSE_PROD', defaultValue: 'compose.prod.yaml')
        string(name: 'COMPOSE_OVERRIDE', defaultValue: 'compose.override.yaml')
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
                script {
                    def hadolintPath = "${WORKSPACE}/tools/hadolint"
                    
                    // Hadolint Installation
                    sh """
                        mkdir -p ${hadolintPath}
                        if ! command -v ${hadolintPath}/hadolint &> /dev/null; then
                            curl -sL -o ${hadolintPath}/hadolint https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64
                            chmod +x ${hadolintPath}/hadolint
                        fi
                    """
                    
                    // Yamllint Installation
                    sh """
                        if ! command -v yamllint &> /dev/null; then
                            pip install --user yamllint
                        fi
                    """
                    
                    // PATH aktualisieren
                    env.PATH = "${hadolintPath}:${env.HOME}/.local/bin:${env.PATH}"
                }
            }
        }
        
        stage('Lint Dockerfiles') {
            steps {
                script {
                    def hadolintPath = "${WORKSPACE}/tools/hadolint"
                    def dockerfiles = sh(script: 'find . -name Dockerfile -o -name "Dockerfile.*"', returnStdout: true).trim().split('\n')
                    dockerfiles.each { dockerfile ->
                        echo "Linting Dockerfile: ${dockerfile}"
                        sh "${hadolintPath}/hadolint ${dockerfile}"
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
    post {
        failure {
            echo 'Pipeline fehlgeschlagen. Überprüfen Sie die Logs für Details zu Linting-Fehlern, Build-Problemen oder Formattierungsproblemen.'
        }
        success {
            echo 'Alle Überprüfungen, Builds und Linting-Prozesse erfolgreich abgeschlossen.'
        }
    }
}
