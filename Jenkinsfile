pipeline {
    agent any

    environment {
        VENV_DIR = 'mlop_env'
        GCP_PROJECT ='utility-ridge-464015-n7'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin/"
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

        stage('Building Docker Image and Pushing to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'Building Docker Image and Pushing to GCR...'
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
        }

        stage('Deploying to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'Deploying to Google Cloud Run...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy mlops-hotel-reservation \
                            --image gcr.io/${GCP_PROJECT}/mlops-hotel-reservation:latest \
                            --platform managed \
                            --region us-central1 \
                            --allow-unauthenticated \

                        '''
                    }
                }
                
            }
        }
    }
}