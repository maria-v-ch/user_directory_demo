#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Run tests and generate coverage report
echo "Running tests"
coverage run -m pytest
coverage report
coverage html

# Create superuser
echo "Creating superuser"
python manage.py create_admin

# Start Gunicorn
echo "Starting Gunicorn"
gunicorn user_directory.wsgi:application --bind 0.0.0.0:8000
