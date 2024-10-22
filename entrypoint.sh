#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create superuser
echo "Creating superuser"
python manage.py create_admin

# Start Gunicorn
echo "Starting Gunicorn"
exec "$@"
