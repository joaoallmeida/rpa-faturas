node {

    stage('Clone repository') {
        checkout scm
    }


    stage('Building Image') {
        app = docker.build('joaoallmeida/rpa-faturas')
    }

    stage('Push Image') {
        docker.withRegistry('https://registry.hub.docker.com','dockerHubCredentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }

    stage('Set Kubernetes Variables') {

        sh "sed -i 's|cronSchedule|${CronJob}|' kubernetes/rpaDeployment.yaml"

    }

    stage('Deploy Kubernetes') {

       kubernetesDeploy(configs: "kubernetes/rpaDeployment.yaml")

    }

}