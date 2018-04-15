source venv/bin/activate

echo "upgrading"
python manage.py db upgrade
