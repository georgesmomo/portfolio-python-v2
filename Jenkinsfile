pipeline {
    agent any // ce pipeline peut être exécuté sur n'importe quel agent Jenkins disponible,

    environment {
        DOCKERHUB_USER = "georgesmomo" // le nom d'utilisateur docker hub
        IMAGE_NAME = "${DOCKERHUB_USER}/porfolio-python-v2" // le nom de l'image docker à créer et pousser sur le hub
        GITHUB_CREDENTIALS = credentials("GITHUB_CREDENTIALS_DEVOPS") // on recupere les credentials github avec la fonction credentials
        DOCKERHUB_CREDENTIALS = credentials("dockerhub_credentials")
        NODEPORT = "30101"
        REPLICAS = "3"
    }

    stages {

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
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage("Prepare kubernetes Deployment files"){
            steps{
                script{
                    sh """
                        cp k8s/deployment.yaml k8s/deployment_tmp.yaml
                        sed -i 's/{{replicas}}/$REPLICAS/g' k8s/deployment_tmp.yaml
                        sed -i 's/{{nodeport}}/$NODEPORT/g' k8s/deployment_tmp.yaml
                        cat k8s/deployment_tmp.yaml
                    """
                }
            }
        }

        stage("Deploy Kubernetes Deployment via Ansible"){
            steps{
                script{
                    //sh """
                      //  ansible-playbook -i ansible/inventory ansible/playbook.yml
                   // """
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