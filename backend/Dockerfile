# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-bullseye

# Expose port 8000
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app/backend

# Install pipenv
RUN pip install -U pipenv

# Install pipenv requirements
COPY Pipfile Pipfile.lock /app/backend/
RUN pipenv install --system
RUN rm -rf ./Pipfile ./Pipfile.lock

# Copy all the code over
COPY . .

# Create the media directory
RUN mkdir -p /app/backend/media

# Create a volume for the media directory
VOLUME /app/backend/media

# Create a volume for the static directory
VOLUME /app/backend/django_static

# Create the data directory
RUN mkdir -p /app/backend/data

# Create a volume for the data directory
VOLUME /app/backend/data

# Make the entrypoint scripts executable
RUN chmod +x /app/backend/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/backend/entrypoint.sh"]