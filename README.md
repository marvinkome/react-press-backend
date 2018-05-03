# ReactPress BackEnd

a simple mini blog api flask and graphql.

### To run locally

```bash
# First clone the repo
git clone https://github.com/marvinkome/react-press-backend

# Activate the virtual environment
cd react-press-backend

source venv/bin/activate # for linux users 
venv/bin/activate # windows users

# Then download dependencies
pip install -r requirements.txt

# Now setup the database
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# Now run the server
python manage.py runserver

```

### Accompanied Project
This project is part of the ReactPress full-stack project.
To see the backend repo, check https://github.com/marvinkome/react-press
