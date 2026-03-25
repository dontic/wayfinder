#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

# run a worker
echo "Starting celery worker..."
celery -A core worker -l info --concurrency 1 -E