node {
    deleteDir()

    stage('Clone Repo') {
        checkout scm
    }

    stage('Building Image') {
        app = docker.build("joaoallmeida/rpa-faturas")
    }

    stage('Push Image') {
        docker.withRegistry('https://registry.hub.docker.com','dockerHubCredentials') {
            app.push("${env.BUILD_NUMBER}")
        }
    }

    stage('Set Kubernetes Variables') {
        withCredentials([usernamePassword(credentialsId: 'enelCredentials', passwordVariable: 'enelPassword', usernameVariable: 'enelUser')
                        , string(credentialsId: 'enelKey', variable: 'enelKey')
                        , usernamePassword(credentialsId: 'brkCredentials', passwordVariable: 'brkPassword', usernameVariable: 'brkUser')]) {
            
            enelUserEncoded = enelUser.bytes.encodeBase64().toString()
            enelPasswordEncoded = enelPassword.bytes.encodeBase64().toString()
            enelKeyEncoded = enelkey.bytes.encodeBase64().toString()
            brkUserEncoded = brkUser.bytes.encodeBase64().toString()
            brkPasswordEncoded = brkPassword.bytes.encodeBase64().toString()

            sh "sed -i 's|cronSchedule|${CronJob}|' Kubernetes/deploy.yaml"
            sh "sed -i 's|latest|${env.BUILD_NUMBER}|' Kubernetes/deploy.yaml"
            sh "sed -i 's|brkUser|brkUserEncoded|' Kubernetes/deploy.yaml"
            sh "sed -i 's|brkPassword|brkPasswordEncoded|' Kubernetes/deploy.yaml"
            sh "sed -i 's|enelUser|enelUserEncoded|' Kubernetes/deploy.yaml"
            sh "sed -i 's|enelPassword|enelPasswordEncoded|' Kubernetes/deploy.yaml"
            sh "sed -i 's|enelKey|brkUserEncoded|' Kubernetes/deploy.yaml"
        }   
    }

    stage('Deploy Kubernetes') {
        withKubeConfig([credentialsId: 'mykubeconfig']) {
            sh 'kubectl apply -f Kubernetes/deploy.yaml'
        } 
    }

}