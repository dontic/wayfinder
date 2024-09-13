# Introduction

This devcontainer will create 3 containers:
- A python container to develop django
- A postgres database
- A redis database (i.e. For celery)

# Configuration

## Postgres Data

Add `postgresdata` to your `.gitignore`. The postgres container will create a `postgresdata` directory inside your `.devcontainer` directory with the database information.

## Postgres configuration

By default postgres will have a database named `django` with user `django` and password `django`. You can modify this in `docker-compose.yml` AND in `provision_postgres.sql`.


# Starting the devcontainer

To start the dev container just run:
```
Dev Containers: Reopen in Container
```

# Initial setup

## Install dependencies
```
pipenv install
```

## Start the environment
```
pipenv shell
```

## Start django
```
python manage.py runserver
```

# Reset the database
To reset the database just go into the Postgres docker container terminal if you have Docker desktop, or by running `docker exec -it <container-id> /bin/sh`

1. Connect to Postgres
```
psql -U django -d postgres
```

2. Remove the `django` database
```
DROP DATABASE django;
```

3. Recreate the `django` database
```
CREATE DATABASE django;
```