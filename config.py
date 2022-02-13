class Config(object):
    # Statement for enabling the development environment
    DEBUG = True
    DEVELOPEMENT = True

    # Statement for enabling new signups
    ENABLE_SIGNUPS = False

    # Define the application directory
    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

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
    SECRET_KEY = "secret"

    # Users database URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False