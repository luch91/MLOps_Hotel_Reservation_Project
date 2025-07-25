pipeline {
    agent any

    environment {
        GCP_PROJECT = 'utility-ridge-464015-n7'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin/"
        IMAGE_NAME = "mlops-hotel-reservation"
        REGION = "us-central1"
    }

    stages {

        stage('Clone Repository') {
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

        stage('Run Training Pipeline') {
            steps {
                echo 'Running training pipeline in a temporary container...'
                sh '''
                    docker run --rm -v $PWD:/app -w /app python:3.10-slim bash -c "
                        apt-get update && apt-get install -y git libgomp1 &&
                        pip install --no-cache-dir -e . &&
                        python pipeline/training_pipeline.py
                    "
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building Docker image and pushing to Google Container Registry (GCR)...'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest .
                            docker push gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying to Google Cloud Run...'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}

                            gcloud run deploy ${IMAGE_NAME} \
                                --image gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:latest \
                                --platform managed \
                                --region ${REGION} \
                                --allow-unauthenticated
                        '''
                    }
                }
            }
        }
    }
}