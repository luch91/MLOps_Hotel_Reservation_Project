pipeline {
    agent any

    environment {
        VENV_DIR = 'mlop_env'
        GCP_PROJECT = 'utility-ridge-464015-n7'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {

        stage('Clone GitHub Repository') {
            steps {
                echo 'Cloning GitHub repository...'
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

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up virtual environment and installing dependencies...'
                sh '''
                    apt update && apt install -y python3 python3-pip python3-venv

                    python3 -m venv ${VENV_DIR}

                    if [ ! -f "${VENV_DIR}/bin/activate" ]; then
                        echo "Virtual environment setup failed!"
                        exit 1
                    fi

                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip

                    if [ -f "requirements.txt" ]; then
                        pip install -r requirements.txt
                    else
                        pip install -e .
                    fi
                '''
            }
        }

        stage('Build Docker Image & Push to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo 'Building Docker image and pushing to Google Container Registry...'
                    sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/mlops-hotel-reservation:latest .
                        docker push gcr.io/${GCP_PROJECT}/mlops-hotel-reservation:latest
                    '''
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo 'Deploying to Google Cloud Run...'
                    sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy mlops-hotel-reservation \
                            --image gcr.io/${GCP_PROJECT}/mlops-hotel-reservation:latest \
                            --platform managed \
                            --region us-central1 \
                            --allow-unauthenticated
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed. Please check the logs for details.'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}