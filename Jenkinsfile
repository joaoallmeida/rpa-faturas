podTemplate(yaml: readTrusted('Kubernetes/docker-deployment.yml')) {
    node(POD_LABEL) {
        stage('Clone Repo') {
            checkout scm
        }
        stage('Docker Login') {
            container('docker') {
                sh 'docker login -u ${DockerUser} -p ${DockerPassword}'
            }
        }
        stage('Build Image') {
            container('docker') {
                sh 'docker build -t joaoallmeida/rpa-faturas .'
            }
        }
        stage('Push Image') {
            container('docker') {
                sh 'docker push -t joaoallmeida/rpa-faturas:${env.BUILD_NUMBER}'
                sh 'docker push -t joaoallmeida/rpa-faturas:latest'
            }
        }
        stage('Deploy K8s') {

            sh 'kubectl apply -f Kubernetes/deploy.yaml'
        
        }
    }
}
