#!/bin/bash

source ./mat_env/bin/activate
python ./matzip_sns/manage.py migrate
python ./matzip_sns/manage.py migrate --run-syncdb
python3 ./matzip_sns/manage.py runserver
