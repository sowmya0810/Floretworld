pipeline {
    agent any

    environment {
        VENV = 'venv'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/your-username/devopsecommerce.git'
            }
        }

        stage('Set up Python Env') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    source $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    source $VENV/bin/activate
                    export FLASK_APP=app.py
                    export FLASK_ENV=development
                    nohup flask run --host=0.0.0.0 --port=5000 &
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline Finished'
        }
    }
}
