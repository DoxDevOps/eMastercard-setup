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

    stage('Fetching emastercard application') {
      steps {
        echo 'Fetching emastercard-updrage-automation'
        sh '[ -d "emastercard-upgrade-automation" ] && echo "App found, skipping cloning." || git clone https://github.com/HISMalawi/emastercard-upgrade-automation.git emastercard-upgrade-automation'
        sh 'echo "Adding permissions for the app to all users" chmod 777 $WORKSPACE/emastercard-upgrade-automation'
      }
    }

    stage('Setup emastercard application') {
      steps {
        echo 'Running setup.py'
        sh 'cd $WORKSPACE/emastercard-upgrade-automation && git pull'
        sh '''cd $WORKSPACE/emastercard-upgrade-automation && echo stf__default1 | sudo -S python3  setup.py
'''
      }
    }

    stage('Shipping application to facility') {
      steps {
        echo 'Shipping eMastercard application to facility'
      }
    }

  }
  environment {
    REQUEST_ID = 'true'
    CLUSTER_ID = '12345'
  }
}