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
    }

    stages {
        stage('Checkout') {
            steps {
                // Récupère le code depuis GitHub en utilisant les credentials configurés.
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv() {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Set Variables based on Branch') {
            steps {
                script {
                    // Détecte le nom de la branche et définit les variables de déploiement en conséquence
                    if (env.BRANCH_NAME == 'develop') {
                        // Si on est sur la branche develop, on déploie sur le port 30099 et 1 réplique
                        env.NODEPORT = "30099"
                        env.REPLICAS = "1"
                    } else if (env.BRANCH_NAME == 'master') {
                        // Si on est sur la branche master, on déploie sur le port 30100 et 2 répliques pour la haute disponibilité
                        env.NODEPORT = "30100"
                        env.REPLICAS = "2"
                    } else {
                        // Pour les autres branches, on peut ne pas déployer automatiquement
                        //error("Branche inconnue pour le déploiement: ${env.BRANCH_NAME}")

                        //par defaut
                        env.NODEPORT = "30100"
                        env.REPLICAS = "2"
                    }
                    // Affiche dans la console les variables pour vérification
                    echo "Déploiement sur le port ${env.NODEPORT} avec ${env.REPLICAS} réplicas"
                }
            }
        }

        stage('Build Docker Image') { 
            steps {
                script {
                    // Construction de l'image Docker à partir du Dockerfile
                    sh """
                    docker build -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Connexion à Docker Hub et push de l'image
                    sh """
                    echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                    docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Prepare Kubernetes Deployment File') {
            steps {
                script {
                    // Ici, on va modifier (via sed ou un outil de templating) le fichier k8s/deployment.yaml
                    // pour remplacer les variables {{ nodeport }} et {{ replicas }} par les valeurs définies
                    sh """
                    cp k8s/deployment.yaml k8s/deployment_tmp.yaml
                    sed -i 's/{{ replicas }}/$REPLICAS/g' k8s/deployment_tmp.yaml
                    sed -i 's/{{ nodeport }}/$NODEPORT/g' k8s/deployment_tmp.yaml
                    mv k8s/deployment_tmp.yaml k8s/deployment.yaml
                    """
                    // Cette étape permet d'adapter le fichier de déploiement en fonction de la branche
                }
            }
        }

        stage('Deploy via Ansible') {
            steps {
                script {
                    sh "whoami"
                    // Utilisation d'Ansible pour déployer l'application sur le master Kubernetes
                    // On exécute le playbook deploy.yml situé dans le dossier ansible
                    sh """
                    ansible-playbook -i ansible/inventory ansible/deploy.yml
                    """
                }
            }
        }
    }

    post {
        always {
            // Nettoyage ou notification à la fin du pipeline
            echo 'Pipeline terminé.'
        }
    }
}


 