#!/bin/bash

source ./mat_env/bin/activate
python3 ./matzip_sns/manage.py migrate
python3 ./matzip_sns/manage.py migrate --run-syncdb
python3 ./matzip_sns/manage.py runserver 0:8000 &
