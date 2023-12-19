node {

    stage('Clone Repo') {
        checkout scm
    }

    stage('Building Image') {
        app = docker.build("joaoallmeida/rpa-faturas")
    }

    stage('Push Image') {
        docker.withRegistry('https://registry.hub.docker.com','dockerHubCredentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }

    stage('Set Kubernetes Variables') {
        sh "sed -i 's|cronSchedule|${CronJob}|' Kubernetes/deploy.yaml"
    }

    stage('Deploy Kubernetes') {
        withKubeConfig([credentialsId: 'mykubeconfig']) {
            sh 'kubectl apply -f Kubernetes/deploy.yaml'
        } 
    }

}

p