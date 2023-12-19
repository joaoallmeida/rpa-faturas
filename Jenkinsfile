node {
    stage('Clone Repo') {
        checkout scm
    }
}
podTemplate(yaml: '''
    apiVersion: v1
    kind: Pod
    spec:
        containers:
        - name: docker
          image: docker:dind
          command:
          - cat
          tty: true
          volumeMounts:
            - mountPath: /var/run/docker.sock
              name: docker-sock
        volumes:
        - name: docker-sock
          hostPath:
            path: /var/run/docker.sock 
    ''' ) {
    node(POD_LABEL) {
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
