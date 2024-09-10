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
                dir('server/client/valentin') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
        // Weitere Stufen...
    }
}
