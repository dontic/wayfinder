# Wayfinder Backend

## How to start developing

1. Open this directory in VSCode or Cursor

2. Make sure you have the `dev containers` extension installed

3. Hit `F1` -> `Reopen in Container` 

4. Once the devcontainer is open, install the dependencies by running `pipenv install`

5. VSCode should detect the venv automatically, if not, run `pipenv shell`

6. Migrate -> `python manage.py migrate`

7. Run the backend -> `python manage.py runserver 0.0.0.0:8000` 