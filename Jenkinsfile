pipeline {
    agent any
    stages {
        stage( 'Docker build' ) {
            steps {
                withCredentials( [
                    file( credentialsId: 'environment_variables', variable: 'ENVIRONMENT_VARIABLES' )
                ] ) {
                   sh "cp \$ENVIRONMENT_VARIABLES .env"
                }
                sh "make container-build"
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
