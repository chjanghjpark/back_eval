mat_env\Scripts\activate.bat && python manage.py migrate && python manage.py migrate --run-syncdb && python matzip_sns\manage.py runserver
