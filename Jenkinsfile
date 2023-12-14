
node {

    stage('Clone Repo') {
        checkout scm
    }

    stage('Building Image') {
        app = docker.build('joaoallmeida/rpa-faturas','-f Docker/Dockerfile --no-cache')
    }

    stage('Push Image') {
        docker.withRegistry('https://registry.hub.docker.com','dockerHubCredentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }

    stage('Set Kubernetes Variables') {

        sh "sed -i 's|cronSchedule|${CronJob}|' Docker/Kubernetes/deploy.yaml"

    }

    stage('Deploy Kubernetes') {

        kubernetesDeploy(configs: 'Docker/Kubernetes/deploy.yaml')

    }

}
