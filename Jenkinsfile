pipeline {
    agent any

    environment{
        VENV_DIR ='mlop_env'
    }

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

        stage('Setting up Virtual Environment and Installing Dependencies') {
            steps {
                
                echo 'Setting up Virtual Environment and Installing Dependencies ....'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate

                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
    }
}
