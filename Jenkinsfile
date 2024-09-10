pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                dir('pfad/zum/react-projekt') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
        // Weitere Stufen...
    }
}
