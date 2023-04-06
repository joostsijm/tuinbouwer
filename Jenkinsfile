pipeline {
    agent { 
            image 'jenkins/agent'
            args '-u 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
            alwaysPull true
        }
    }
    stages {
        stage( 'Docker build' ) {
            steps {
                withCredentials( [
                    file( credentialsId: 'environment_variables', variable: 'ENVIRONMENT_VARIABLES' )
                ] ) {
                   sh "cp \$ENVIRONMENT_VARIABLES .env"
                }
                sh "make build"
            }
        }
        stage( 'Docker save' ) {
            steps {
                sh "make container-save"
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'container.tar', fingerprint: true
        }
    }
}
