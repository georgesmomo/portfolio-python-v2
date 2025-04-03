// Jenkinsfile - Pipeline declaratif pour le déploiement automatique
pipeline {
    agent any   // Le pipeline peut s'exécuter sur n'importe quel agent Jenkins disponible

    environment {
        // Variables globales du pipeline 
        DOCKERHUB_USER = "georgesmomo"    // Nom d'utilisateur Docker Hub
        IMAGE_NAME = "${DOCKERHUB_USER}/portfolio-python"
        // Les credentials pour GitHub et Docker Hub sont définis dans Jenkins   
        GITHUB_CREDENTIALS = credentials('GITHUB_CREDENTIALS_DEVOPS')
        DOCKERHUB_CREDENTIALS = credentials('dockerhub_credentials')
        NODEPORT = "30101"
        REPLICAS = "3"
    }

    stages {
        stage('Checkout code source2') {
            steps {
                // on recupere le code source de github 
                echo "test..."
            }
        }
        stage('Checkout code source') {
            steps {
                // on recupere le code source de github 
                checkout scm
            }
        }

        stage('Build the docker image') {
            steps {
                script {
                    sh """
                        docker build -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }

        stage("Push docker image to docker hub") {
            steps {
                script {
                    sh """
                        echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                    """
                }
            }
        }

    }

    post {
        always {
            echo "Terminé!!!"
        }
    }

}