pipeline {
    agent { 
            image 'jenkins/agent'
            args '-u 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
            alwaysPull true
        }
    }
}
