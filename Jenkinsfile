pipeline {
  agent {
    kubernetes {
      yamlFile 'Kubernetes/docker-deployment.yml'
      retries 2
    }
  }
  stages {
    stage('Clone') {
      steps {
        checkout scm
      }
    } 
    stage('Docker Login') {
        steps {
            container('docker') {
                sh 'docker login -u ${DockerUser} -p ${DockerPassword}'
            }
        }
    } 
    stage('Build Image') {
      steps {
        container('docker') {
          sh 'docker build -t joaoallmeida/rpa-faturas .'
        }
      }
    }
     stage('Push Images') {
      steps {
        container('docker') {
            sh 'docker push -t joaoallmeida/rpa-faturas:${env.BUILD_NUMBER}'
            sh 'docker push -t joaoallmeida/rpa-faturas:latest'
        }
    }
    }
  }
    post {
      always {
        container('docker') {
          sh 'docker logout'
      }
      }
    }
}