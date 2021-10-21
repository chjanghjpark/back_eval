#!/bin/bash

python3 -m venv mat_env
source ./mat_env/bin/activate
pip install -r requirements.txt
pip list
