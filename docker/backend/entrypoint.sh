#!/bin/bash

./deploy.sh 2 0 0 0 0

source .env/bin/activate

cd backend
gunicorn Main.wsgi:application --bind 0.0.0.0:8000

# To get interactive terminal in the container
# /bin/bash