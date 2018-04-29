web: gunicorn manage:app
release: python manage.py db migrate && python manage.py db migrate && python manage.py db upgrade