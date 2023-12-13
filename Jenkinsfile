node {

    stage('Clone repository') {
        checkout scm
    }

    stage('Building Image') {
        app = docker.build('joaoallmeida/rpa-faturas')
    }

    stage('Push Image'){
        docker.withRegistry('https://registry.hub.docker.com','dockerHubCredentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }

}