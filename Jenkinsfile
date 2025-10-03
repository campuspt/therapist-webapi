pipeline {
    agent any

    environment {
        REGISTRY = "registry.campusphysicaltherapy.com"
        APP_NAME = "therapist-webapi"
        IMAGE = "${REGISTRY}/${APP_NAME}:latest"

        // Credentials (managed by Jenkins)
        API_SECRET_KEY = credentials('API_SECRET_KEY')
        KUBECONFIG_FILE = credentials('KUBECONFIG_FILE')

        // Parameters (from job config)
        DB_NAME_MAIN = "${params.DB_NAME_MAIN}"
        DB_NAME = "${params.DB_NAME}"
        DB_USER = "${params.DB_USER}"
        DB_PASS = "${params.DB_PASS}"
        DB_HOST = "${params.DB_HOST}"
        DB_PORT = "${params.DB_PORT}"
        REMINDERS_WEBAPI = "${params.REMINDERS_WEBAPI}"
        NETWORK_SEGMENT = "${params.NETWORK_SEGMENT}"
        FRONTEND_WEBAPP_URL = "${params.FRONTEND_WEBAPP_URL}"
        DEBUG = "${params.DEBUG}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "[INFO] Checking out source code..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "[INFO] Building Docker image..."
                sh '''
                    cd ${WORKSPACE}/therapist-webapi
                    docker build -t ${IMAGE} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "[INFO] Pushing image to ${REGISTRY}..."
                sh 'docker push ${IMAGE}'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "[INFO] Using kubeconfig from Jenkins secret..."
                sh '''
                    export KUBECONFIG=$KUBECONFIG_FILE
                    echo "[INFO] Checking cluster access..."
                    kubectl cluster-info
                '''

                echo "[INFO] Creating/Updating Secrets..."
                sh '''
                    kubectl -n default create secret generic db-secrets \
                      --from-literal=API_SECRET_KEY="${API_SECRET_KEY}" \
                      --from-literal=DB_NAME_MAIN="${DB_NAME_MAIN}" \
                      --from-literal=DB_NAME="${DB_NAME}" \
                      --from-literal=DB_USER="${DB_USER}" \
                      --from-literal=DB_PASS="${DB_PASS}" \
                      --from-literal=DB_HOST="${DB_HOST}" \
                      --from-literal=DB_PORT="${DB_PORT}" \
                      --from-literal=REMINDERS_WEBAPI="${REMINDERS_WEBAPI}" \
                      --from-literal=NETWORK_SEGMENT="${NETWORK_SEGMENT}" \
                      --from-literal=FRONTEND_WEBAPP_URL="${FRONTEND_WEBAPP_URL}" \
                      --from-literal=DEBUG="${DEBUG}" \
                      --dry-run=client -o yaml | kubectl apply -f -
                '''

                echo "[INFO] Applying Kubernetes manifests..."
                sh '''
                    kubectl apply -f ${WORKSPACE}/therapist-webapi/k8s/deployment.yaml
                    kubectl apply -f ${WORKSPACE}/therapist-webapi/k8s/service.yaml

                    echo "[INFO] Waiting for rollout..."
                    kubectl rollout status deployment/${APP_NAME} --timeout=180s
                '''
            }
        }
    }

    post {
        success {
            echo "[SUCCESS] Deployment completed successfully!"
        }
        failure {
            echo "[ERROR] Pipeline failed."
        }
    }
}
