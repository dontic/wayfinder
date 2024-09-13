#!/bin/bash

echo "Migrating..."

python manage.py migrate --no-input

echo "Collecting static files..."

python manage.py collectstatic --no-input

# Ensure the data directory exists
mkdir -p data

echo "Starting server..."

gunicorn core.wsgi:application --forwarded-allow-ips="*" --bind 0.0.0.0:8000

#####################################################################################
# Options to DEBUG Django server
# Optional commands to replace abouve gunicorn command

# Option 1:
# run gunicorn with debug log level
# gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 1 --threads 1 --log-level debug

# Option 2:
# run development server
# DEBUG=True ./manage.py runserver 0.0.0.0:8000