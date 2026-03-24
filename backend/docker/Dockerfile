FROM python:3.11-bullseye

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend

# Install pipenv
RUN pip install -U pipenv

# Copy only dependency files first (for better cache efficiency)
COPY Pipfile Pipfile.lock /app/backend/

# Install dependencies (this layer will be cached unless Pipfile changes)
RUN pipenv requirements > requirements.txt && \
    pip install -r requirements.txt && \
    rm -rf ./Pipfile ./Pipfile.lock ./requirements.txt

# Create directories and volumes (these rarely change)
RUN mkdir -p /app/backend/media

VOLUME /app/backend/media
VOLUME /app/backend/django_static

# Copy all the code (this should be last to maximize cache hits)
COPY . .

# Set permissions on entrypoint scripts (after copying code)
RUN chmod +x /app/backend/docker/entrypoint-django.sh && \
    chmod +x /app/backend/docker/entrypoint-worker.sh && \
    chmod +x /app/backend/docker/entrypoint-beat.sh

ENTRYPOINT ["/app/backend/docker/entrypoint-django.sh"]