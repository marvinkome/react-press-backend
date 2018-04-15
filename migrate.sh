source venv/bin/activate

echo "migrating"
python manage.py db migrate
