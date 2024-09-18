"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import logging.config

# Load environment variables
load_dotenv()

# ---------------------------------------------------------------------------- #
#                                     PATHS                                    #
# ---------------------------------------------------------------------------- #

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if "BASE_URL" not in os.environ:
    raise ValueError("BASE_URL environment variable not set.")

# I.e.: http://localhost:8000, https://example.com
BASE_URL = os.getenv("BASE_URL")

BASE_URL_PROTOCOL = BASE_URL.split("://")[0]
BASE_URL_HOST = BASE_URL.split("://")[1].split(":")[0]
BASE_URL_PORT = BASE_URL.split("://")[1].split(":")[1]

PARSED_ALLOWED_HOSTS = [BASE_URL_HOST]
PARSED_ALLOWED_ORIGINS = [BASE_URL]
PARSED_CORS_ORIGIN_WHITELIST = [BASE_URL]
PARSED_DJANGO_CSRF_COOKIE_DOMAIN = BASE_URL_HOST
PARSED_DJANGO_SESSION_COOKIE_DOMAIN = BASE_URL_HOST


# ---------------------------------------------------------------------------- #
#                                   DEBUGGING                                  #
# ---------------------------------------------------------------------------- #

# Optional environment variable, if not set, default to True
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

# Logging
LOGGING_CONFIG = None  # Avoid Django logging setup
LOGGING = {
    "version": 1,
    # Set to True to disable Django's logging setup
    "disable_existing_loggers": True,
    # Define the formatters
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    # Define the handlers
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",  # Log to console
            "formatter": "default",  # Use the default formatter
        }
    },
    # Uncomment to log with the root logger
    # "root": {"level": "WARNING", "handlers": ["console"]},
    "loggers": {
        # Consistent logger for the application
        # Use `log = logging.getLogger("app_logger")` in your code
        "app_logger": {
            "level": os.getenv("LOGGING_LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": False,
        },
        # Django logger
        "django": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        # Celery logger
        "celery": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        # Celery beat logger
        "celery.beat": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING)


# ---------------------------------------------------------------------------- #
#                                  CONNECTIONS                                 #
# ---------------------------------------------------------------------------- #
# SECURITY WARNING: keep the secret key used in production secret!
if "DJANGO_SECRET_KEY" not in os.environ:
    raise ValueError("DJANGO_SECRET_KEY environment variable not set.")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Hosts

ALLOWED_HOSTS = PARSED_ALLOWED_HOSTS

# CSRF
CSRF_TRUSTED_ORIGINS = PARSED_ALLOWED_ORIGINS

CSRF_COOKIE_NAME = "csrftoken"

CSRF_COOKIE_DOMAIN = PARSED_DJANGO_CSRF_COOKIE_DOMAIN

CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True

# CORS settings
CORS_ORIGIN_WHITELIST = PARSED_CORS_ORIGIN_WHITELIST

CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True

# Sessions
SESSION_COOKIE_DOMAIN = PARSED_DJANGO_SESSION_COOKIE_DOMAIN

SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework.authtoken",
    # ----------------------------------- CORS ----------------------------------- #
    "corsheaders",  # Django CORS Headers
    # ----------------------------------- REST ----------------------------------- #
    "rest_framework",  # Django REST Framework
    "drf_spectacular",  # Django Spectacular
    # ----------------------------------- Apps ----------------------------------- #
    "wayfinder",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Django CORS Headers
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------------------- #
#                                     WSGI                                     #
# ---------------------------------------------------------------------------- #
WSGI_APPLICATION = "core.wsgi.application"


# ---------------------------------------------------------------------------- #
#                                   DATABASE                                   #
# ---------------------------------------------------------------------------- #

# Uses the `timescale.db.backends.postgresql` backend
# Defaults to using the timescaledb container
# The defaults are:
# - database = django
# - user =     django
# - password = django
DATABASES = {
    "default": {
        "ENGINE": "timescale.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "django"),
        "USER": os.getenv("POSTGRES_USER", "django"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "django"),
        "HOST": os.getenv("POSTGRES_HOST", "timescaledb"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------- #
#                                AUTHENTICATION                                #
# ---------------------------------------------------------------------------- #

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ---------------------------------------------------------------------------- #
#                             Internationalization                             #
# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ---------------------------------------------------------------------------- #
#                            STATIC AND MEDIA ROUTES                           #
# ---------------------------------------------------------------------------- #

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"

# ---------------------------------------------------------------------------- #
#                                REST FRAMEWORK                                #
# ---------------------------------------------------------------------------- #

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # "DEFAULT_THROTTLE_CLASSES": [
    #     "rest_framework.throttling.AnonRateThrottle",
    #     "rest_framework.throttling.UserRateThrottle",
    #     "rest_framework.throttling.ScopedRateThrottle",
    # ],
    # "DEFAULT_THROTTLE_RATES": {
    #     "dj_rest_auth": "30/hour",
    #     "anon": "10/hour",
    #     "user": "200/minute",
    # },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "Description placeholder",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}
