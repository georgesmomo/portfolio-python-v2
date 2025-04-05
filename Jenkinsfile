pipeline {
    agent any // ce pipeline peut être exécuté sur n'importe quel agent Jenkins disponible,

    environment {
        DOCKERHUB_USER = "georgesmomo" // le nom d'utilisateur docker hub
        IMAGE_NAME = "${DOCKERHUB_USER}/portfolio-python-v2" // le nom de l'image docker à créer et pousser sur le hub
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
                        pwd
                        cat k8s/deployment_tmp.yaml

                    """
                }
            }
        }

        stage("Deploy Kubernetes Deployment via ssh") {
            steps {
                script {
                    // Affiche l'utilisateur et le répertoire courant pour débogage
                    sh """
                        whoami
                        pwd
                        # Copie du fichier sur le serveur distant
                        scp -i ~/.ssh/id_rsa_kube_050425_2 k8s/deployment_tmp.yaml root@207.180.212.38:/tmp/deployment.yaml
                        # Applique le déploiement et redémarre le déploiement Kubernetes
                        ssh -i ~/.ssh/id_rsa_kube_050425_2 root@207.180.212.38 'microk8s.kubectl apply -f /tmp/deployment.yaml && microk8s.kubectl rollout restart deployment/portfolio-v2-deployment && microk8s.kubectl rollout status deployment/portfolio-v2-deployment'
                    """
                }
            }
        }



        /*stage("Deploy Kubernetes Deployment via Ansible"){
            steps{
                script{
                    //echo "Playbook ansible"
                    sh """
                        whoami
                        pwd
                        ansible-playbook -i ansible/inventory ansible/playbook.yml
                    """
                }
            }
        }*/

    }

    post {
        always {
            cleanWs()
            echo "Dossier de travail nettoyé. Terminé!!!"
        }
    }

}