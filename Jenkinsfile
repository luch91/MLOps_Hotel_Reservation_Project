pipeline {
    agent any

    stages {
        stage('Cloning GitHub repo to Jenkins workspace') {
            steps {
                echo 'Cloning GitHub repo to Jenkins...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/luch91/MLOps_Hotel_Reservation_Project.git',
                        credentialsId: 'github-token'
                    ]]
                ])
            }
        }
    }
}
