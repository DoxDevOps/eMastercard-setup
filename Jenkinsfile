pipeline {
  agent any
  stages {
    stage('Initializing') {
      steps {
        echo 'Initializing ...'
        sh 'echo "Working from $WORKSPACE"'
        sh '''echo "Your build number is: \\${BUILD_NUMBER} -> ${BUILD_NUMBER}"
echo "Your build number is: \\${REQUEST_ID} -> ${REQUEST_ID}"'''
      }
    }

    stage('Test') {
      steps {
        echo 'Test'
      }
    }

  }
  environment {
    REQUEST_ID = 'true'
    CLUSTER_ID = '12345'
  }
}