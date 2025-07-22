pipeline{
    agent any

    stages {
        stage('Cloning GitHub repo to Jenkins workspace') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins......'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/luch91/MLOps_Hotel_Reservation_Project.git']])

                }
                
                // Add build steps here
            }
        }
        
    }
}