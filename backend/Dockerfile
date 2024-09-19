# Stage 1: Build dependencies
FROM python:3.11-bullseye as builder

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv requirements > requirements.txt


# Stage 2: Final image
FROM python:3.11-bullseye

WORKDIR /app

# Copy only the requirements file from the builder stage
COPY --from=builder /app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

RUN ls

# Make the entrypoint scripts executable
RUN chmod +x /app/entrypoint-django.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint-django.sh"]
