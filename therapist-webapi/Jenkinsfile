pipeline {
    agent any

    environment {
        REGISTRY = "registry.campusphysicaltherapy.com"
        APP_NAME = "therapist-webapi"
        IMAGE = "${REGISTRY}/${APP_NAME}:latest"

        // Jenkins environment variables (must be configured in Jenkins -> Manage Credentials or Job Parameters)
        API_SECRET_KEY = credentials('API_SECRET_KEY')
        DB_NAME_MAIN = credentials('DB_NAME_MAIN')
        DB_NAME = credentials('DB_NAME')
        DB_USER = credentials('DB_USER')
        DB_PASS = credentials('DB_PASS')
        DB_HOST = credentials('DB_HOST')
        DB_PORT = "3306"
        PORT_NUMBER = credentials('PORT_NUMBER')
        DEBUG = credentials('DEBUG')
        PROJECT_NAME = credentials('PROJECT_NAME')
        ENVIROMENT = credentials('ENVIROMENT')
        REMINDERS_WEBAPI = credentials('REMINDERS_WEBAPI')
        NETWORK_SEGMENT = credentials('NETWORK_SEGMENT')
        FRONTEND_WEBAPP_URL = credentials('FRONTEND_WEBAPP_URL')

        // Kubeconfig path (the secret file path stored in Jenkins credentials or env)
        KUBECONFIG_FILE = "kubeconfig-campuspt"
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
                echo "[INFO] Exporting kubeconfig..."
                // Note: We assume your Jenkins secret or env already stores the kubeconfig path or file
                sh '''
                    if [ ! -f "$KUBECONFIG_FILE" ]; then
                        echo "[ERROR] kubeconfig not found: $KUBECONFIG_FILE"
                        exit 1
                    fi
                    export KUBECONFIG=$KUBECONFIG_FILE
                    echo "[INFO] Using kubeconfig: $KUBECONFIG"
                    kubectl cluster-info
                '''

                echo "[INFO] Applying Kubernetes Secrets..."
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
                      --dry-run=client -o yaml | kubectl apply -f -
                '''

                echo "[INFO] Applying Kubernetes Deployment and Service..."
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
            echo "[SUCCESS] Deployment completed successfully "
        }
        failure {
            echo "[ERROR] Pipeline failed "
        }
    }
}
