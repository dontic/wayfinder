class Config(object):
    ###### GENERAL ######
    # Statement for enabling new signups
    ENABLE_SIGNUPS = True

    # Number of database backup versions after cleanup
    N_BACKUPS = 2


    ###### PATH MAP ######
    # Default time span for path map plot in days (days back from now)
    DAYS_PERIOD_PATH = 7

    # Max number of days to query in path map
    MAX_QUERY_DAYS_PATH = 30

    # Max accuracy value for path map points, default = 10 meters
    # This will delete any points that have accuracy > MAX_ACCURACY_PATH
    MAX_ACCURACY_PATH = 10


    ###### VISITS MAP ######
    # Ignore home location in visits map by default
    IGNORE_HOME = True

    # Default time span for map plots in days (days back to now)
    DAYS_PERIOD_VISITS = 7

    # Max number of days to query in visits map
    MAX_QUERY_DAYS_VISITS = 30


    ###### OTHER VARIABLES ######
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