#!/bin/bash

#create a venv
python3 -m venv venv
source venv/bin/activate

# Install/update Python packages
pip3 install -r requirements.txt

# Navigate to the root directory of your Django project
cd backend
python3 manage.py runserver

"""
# Activate the virtual environment (if you have one)
# source /path/to/your/virtualenv/bin/activate

# Install/update Python packages
pip install -r requirements.txt

# Apply Django database migrations
python manage.py migrate

# Collect static files (if needed)
# python manage.py collectstatic --noinput

# Start Gunicorn application server
gunicorn your_project_name.wsgi:application -b 0.0.0.0:8000
"""