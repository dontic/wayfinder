#!/bin/bash

echo "Migrating..."

python manage.py migrate --no-input

echo "Collecting static files..."

python manage.py collectstatic --no-input

# Check if superuser exists and create one if it doesn't
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]
then
    echo "Checking for existing superuser..."
    if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.filter(is_superuser=True).exists())"
    then
        echo "Superuser already exists. Skipping creation."
    else
        echo "Creating superuser..."
        python manage.py createsuperuser \
            --noinput \
            --username $DJANGO_SUPERUSER_USERNAME \
            --email $DJANGO_SUPERUSER_EMAIL
        echo "Superuser created successfully!"
    fi
else
    echo "Superuser environment variables not set. Skipping superuser creation."
fi

echo "Starting server..."

gunicorn core.wsgi:application --forwarded-allow-ips="*" --bind 0.0.0.0:8000

#####################################################################################
# Options to DEBUG Django server
# Optional commands to replace above gunicorn command

# Option 1:
# run gunicorn with debug log level
# gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 1 --threads 1 --log-level debug

# Option 2:
# run development server
# DEBUG=True ./manage.py runserver 0.0.0.0:8000