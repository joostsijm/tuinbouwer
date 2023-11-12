pipeline {
    agent {
        docker {
            image 'docker:latest'
            args '-u 0:0 -v /var/run/docker.sock:/var/run/docker.sock '
            alwaysPull true
        }
    }
    stages {
        stage( 'Docker build' ) {
            steps {
                withCredentials( [
                    file( credentialsId: 'tuinbouwer_env', variable: 'ENVIRONMENT_VARIABLES' )
                ] ) {
                   sh "cp \$ENVIRONMENT_VARIABLES .env"
                }
                sh "docker build -t tuinbouwer ."
            }
        }
        stage( 'Docker save' ) {
            steps {
                sh "docker save tuinbouwer -o container.tar"
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'container.tar', fingerprint: true
        }
    }
}
