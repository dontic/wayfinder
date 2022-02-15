class Config(object):
    # Statement for enabling new signups
    ENABLE_SIGNUPS = True

    # Ignore home location in visits map by default
    IGNORE_HOME = True

    # Default time span for map plots in days (days back to now)
    DAYS_PERIOD = 7

    # Define the application directory
    from pathlib import Path
    BASE_DIR = Path.cwd()

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data. 
    CSRF_SESSION_KEY = "secret"

    # Secret key for signing cookies
    SECRET_KEY = "super_secret"

    # Users database URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Statement for enabling the development environment
    DEBUG = True
    DEVELOPEMENT = True